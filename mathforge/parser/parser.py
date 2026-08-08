"""
mathforge/parser/parser.py

Parser

Recursive-descent parser: converts a token list (from tokenizer.py) into an AST (ast_nodes.py), respecting operator precedence.

Grammar (highest-level rule first):

    expression := term (("+" | "-") term)*
    term       := factor (("*" | "/") factor)*
    factor     := NUMBER | "(" expression ")" | "-" factor

Each rule is implemented as one method below. A rule calls the rule(s) beneath it in this list, which is what makes '*' bind tighter than '+' — by the time parse_expression() sees the '+', its two operands (parsed via parse_term) have already fully absorbed any '*'/'/' around them.
"""

from mathforge.parser.tokenizer import tokenize, TokenType
from mathforge.parser.ast_nodes import Number, BinaryOp
from mathforge.core.errors import ParserError


class Parser:
    """
    Builds an AST from a token list, one token at a time.

    Holds a position (self._pos) into the token list and always looks at self._current() to decide what to do next — this "look at the next token, then decide" style is standard for recursive-descent parsers.
    """

    def __init__(self, tokens: list):
        """
        Parameters
        ----------
        tokens : list of Token
            As produced by tokenizer.tokenize(). Must end in an
            EOF token.
        """
        self._tokens = tokens
        self._pos = 0

    @classmethod
    def from_string(cls, source: str) -> "Parser":
        """
        Convenience constructor: tokenize a string and build a Parser from the result.

        Parameters
        ----------
        source : str

        Returns
        -------
        Parser
        """
        return cls(tokenize(source))

    def _current(self):
        """Return the token at the current position, without consuming it."""
        return self._tokens[self._pos]

    def _advance(self):
        """Return the current token and move the position forward by one."""
        token = self._tokens[self._pos]
        self._pos += 1
        return token

    def _expect(self, token_type: str):
        """
        Consume the current token if it matches token_type, else raise ParserError. Used for tokens whose presence is required by the grammar but whose value we don't need
        """
        if self._current().type != token_type:
            raise ParserError(
                f"expected {token_type} but got {self._current().type} "
                f"at position {self._pos}"
            )
        return self._advance()

    def parse(self):
        """
        Parse the full token list into an AST, and confirm nothing
        is left over afterward.

        Returns
        -------
        Number or BinaryOp
            The root of the parsed expression tree.

        Raises
        ------
        ParserError
            If the input is malformed, or there are leftover tokens after a complete expression (e.g. "3 + 4)").
        """
        result = self.parse_expression()
        self._expect(TokenType.EOF)
        return result

    def parse_expression(self):
        """
        expression := term (("+" | "-") term)*

        Returns
        -------
        Number or BinaryOp
        """
        node = self.parse_term()

        while self._current().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self._advance()
            operator = "+" if op_token.type == TokenType.PLUS else "-"
            right = self.parse_term()
            node = BinaryOp(operator, node, right)

        return node

    def parse_term(self):
        """
        term := factor (("*" | "/") factor)*

        Returns
        -------
        Number or BinaryOp
        """
        node = self.parse_factor()

        while self._current().type in (TokenType.STAR, TokenType.SLASH):
            op_token = self._advance()
            operator = "*" if op_token.type == TokenType.STAR else "/"
            right = self.parse_factor()
            node = BinaryOp(operator, node, right)

        return node

    def parse_factor(self):
        """
        factor := NUMBER | "(" expression ")" | "-" factor

        Returns
        -------
        Number or BinaryOp

        Raises
        ------
        ParserError
            If the current token is none of the above (e.g. an unexpected operator, or running out of tokens early).
        """
        token = self._current()

        if token.type == TokenType.NUMBER:
            self._advance()
            return Number(token.value)

        if token.type == TokenType.LPAREN:
            self._advance()
            node = self.parse_expression()
            self._expect(TokenType.RPAREN)
            return node

        if token.type == TokenType.MINUS:
            self._advance()
            operand = self.parse_factor()
            return BinaryOp("-", Number(0.0), operand)

        raise ParserError(f"unexpected token {token.type} at position {self._pos}")
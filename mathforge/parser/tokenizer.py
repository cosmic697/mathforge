"""
mathforge/parser/tokenizer.py

Tokenizer

Converts a raw expression string into a flat list of Tokens —
the first stage of parsing, before precedence/structure is applied.
"""

from mathforge.core.errors import ParserError


class TokenType:
    """
    Enumeration of token kinds. Plain class with class-level string
    constants — deliberately not Python's `enum` module, to keep
    this simple and match the "avoid unnecessary library reliance"
    philosophy for now.
    """
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"  # marks the end of input — makes the parser's
                 # "am I done yet?" check uniform, instead of a
                 # special case for running off the end of the list


class Token:
    """
    A single token: a type, and the literal value (if any).

    Attributes
    ----------
    type : str
        One of the TokenType constants.
    value : float or None
        The numeric value, only set for NUMBER tokens. None for
        everything else (operators, parens, EOF carry no value —
        their type alone is the information).
    """

    def __init__(self, type_: str, value=None):
        """
        Parameters
        ----------
        type_ : str
            A TokenType constant.
        value : float or None, optional
        """
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            "Token(TYPE)" or "Token(TYPE, value)" if value is set.
        """
        if self.value is not None:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"

    def __eq__(self, other: object) -> bool:
        """
        Two tokens are equal if their type and value both match.
        Mainly here so tests can compare token lists directly with
        == instead of checking .type/.value by hand.
        """
        if not isinstance(other, Token):
            return NotImplemented
        return self.type == other.type and self.value == other.value


_SINGLE_CHAR_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
}


def tokenize(source: str) -> list:
    """
    Convert an expression string into a list of Tokens.

    Parameters
    ----------
    source : str
        The raw expression, e.g. "3 + 4 * 2".

    Returns
    -------
    list of Token
        Ends with a single Token(TokenType.EOF).

    Raises
    ------
    ParserError
        If an unrecognized character is encountered, or a number
        is malformed (e.g. "3.4.5", or a lone "." with no digits).
    """
    tokens = []
    i = 0
    n = len(source)

    while i < n:
        ch = source[i]

        if ch.isspace():
            i += 1
            continue

        if ch in _SINGLE_CHAR_TOKENS:
            tokens.append(Token(_SINGLE_CHAR_TOKENS[ch]))
            i += 1
            continue

        if ch.isdigit() or ch == ".":
            start = i
            seen_dot = False
            while i < n and (source[i].isdigit() or source[i] == "."):
                if source[i] == ".":
                    if seen_dot:
                        raise ParserError(f"malformed number near position {start}: '{source[start:i+1]}'")
                    seen_dot = True
                i += 1
            text = source[start:i]
            if text == ".":
                raise ParserError(f"malformed number near position {start}: '.'")
            tokens.append(Token(TokenType.NUMBER, float(text)))
            continue

        raise ParserError(f"unexpected character '{ch}' at position {i}")

    tokens.append(Token(TokenType.EOF))
    return tokens
"""
mathforge/parser/tests/test_tokenizer.py

Unit tests for the Tokenizer.
"""

import pytest

from mathforge.parser.tokenizer import tokenize, Token, TokenType
from mathforge.core.errors import ParserError


def test_single_number():
    assert tokenize("3") == [Token(TokenType.NUMBER, 3.0), Token(TokenType.EOF)]


def test_decimal_number():
    assert tokenize("3.14") == [Token(TokenType.NUMBER, 3.14), Token(TokenType.EOF)]


def test_simple_addition():
    assert tokenize("3 + 4") == [
        Token(TokenType.NUMBER, 3.0),
        Token(TokenType.PLUS),
        Token(TokenType.NUMBER, 4.0),
        Token(TokenType.EOF),
    ]


def test_all_operators():
    assert tokenize("1+2-3*4/5") == [
        Token(TokenType.NUMBER, 1.0),
        Token(TokenType.PLUS),
        Token(TokenType.NUMBER, 2.0),
        Token(TokenType.MINUS),
        Token(TokenType.NUMBER, 3.0),
        Token(TokenType.STAR),
        Token(TokenType.NUMBER, 4.0),
        Token(TokenType.SLASH),
        Token(TokenType.NUMBER, 5.0),
        Token(TokenType.EOF),
    ]


def test_parentheses():
    assert tokenize("(1 + 2)") == [
        Token(TokenType.LPAREN),
        Token(TokenType.NUMBER, 1.0),
        Token(TokenType.PLUS),
        Token(TokenType.NUMBER, 2.0),
        Token(TokenType.RPAREN),
        Token(TokenType.EOF),
    ]


def test_ignores_extra_whitespace():
    assert tokenize("   3   +   4  ") == [
        Token(TokenType.NUMBER, 3.0),
        Token(TokenType.PLUS),
        Token(TokenType.NUMBER, 4.0),
        Token(TokenType.EOF),
    ]


def test_empty_string_returns_only_eof():
    assert tokenize("") == [Token(TokenType.EOF)]


def test_unexpected_character_raises():
    with pytest.raises(ParserError):
        tokenize("3 + $")


def test_malformed_number_two_dots_raises():
    with pytest.raises(ParserError):
        tokenize("3.4.5")


def test_lone_dot_raises():
    with pytest.raises(ParserError):
        tokenize(".")


def test_token_repr_with_value():
    assert repr(Token(TokenType.NUMBER, 3.0)) == "Token(NUMBER, 3.0)"


def test_token_repr_without_value():
    assert repr(Token(TokenType.PLUS)) == "Token(PLUS)"
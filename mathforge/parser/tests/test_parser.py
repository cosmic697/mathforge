"""
mathforge/parser/tests/test_parser.py

Unit tests for the Parser.
"""

import pytest

from mathforge.parser.parser import Parser
from mathforge.parser.ast_nodes import Number, BinaryOp
from mathforge.core.errors import ParserError


def parse(source: str):
    return Parser.from_string(source).parse()


def test_single_number():
    assert parse("3") == Number(3.0)


def test_simple_addition():
    assert parse("3 + 4") == BinaryOp("+", Number(3.0), Number(4.0))


def test_precedence_multiplication_before_addition():
    # 3 + 4 * 2 should parse as 3 + (4 * 2), NOT (3 + 4) * 2
    expected = BinaryOp("+", Number(3.0), BinaryOp("*", Number(4.0), Number(2.0)))
    assert parse("3 + 4 * 2") == expected


def test_precedence_division_before_subtraction():
    expected = BinaryOp("-", Number(10.0), BinaryOp("/", Number(6.0), Number(2.0)))
    assert parse("10 - 6 / 2") == expected


def test_left_associativity():
    # 10 - 3 - 2 should parse as (10 - 3) - 2, not 10 - (3 - 2)
    expected = BinaryOp("-", BinaryOp("-", Number(10.0), Number(3.0)), Number(2.0))
    assert parse("10 - 3 - 2") == expected


def test_parentheses_override_precedence():
    # (3 + 4) * 2 should parse with the + grouped first
    expected = BinaryOp("*", BinaryOp("+", Number(3.0), Number(4.0)), Number(2.0))
    assert parse("(3 + 4) * 2") == expected


def test_nested_parentheses():
    expected = BinaryOp("*", Number(2.0), BinaryOp("+", Number(1.0), Number(3.0)))
    assert parse("2 * (1 + 3)") == expected


def test_unary_minus():
    expected = BinaryOp("-", Number(0.0), Number(5.0))
    assert parse("-5") == expected


def test_unary_minus_in_expression():
    expected = BinaryOp("+", Number(3.0), BinaryOp("-", Number(0.0), Number(2.0)))
    assert parse("3 + -2") == expected


def test_unmatched_open_paren_raises():
    with pytest.raises(ParserError):
        parse("(3 + 4")


def test_unmatched_close_paren_raises():
    with pytest.raises(ParserError):
        parse("3 + 4)")


def test_trailing_garbage_raises():
    with pytest.raises(ParserError):
        parse("3 + 4 5")


def test_empty_input_raises():
    with pytest.raises(ParserError):
        parse("")


def test_dangling_operator_raises():
    with pytest.raises(ParserError):
        parse("3 +")
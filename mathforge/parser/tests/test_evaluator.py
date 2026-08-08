"""
mathforge/parser/tests/test_evaluator.py

Unit tests for the Evaluator (Fraction-based).
"""

import pytest

from mathforge.parser.evaluator import evaluate, evaluate_string
from mathforge.parser.ast_nodes import Number, BinaryOp
from mathforge.arithmetic.numbers.fraction import Fraction
from mathforge.core.errors import UndefinedOperationError, InvalidOperandError, ParserError


# --- evaluate() on hand-built trees ---

def test_evaluate_number():
    assert evaluate(Number(5.0)) == Fraction(5)


def test_evaluate_simple_add():
    assert evaluate(BinaryOp("+", Number(3.0), Number(4.0))) == Fraction(7)


def test_evaluate_nested():
    tree = BinaryOp("+", Number(3.0), BinaryOp("*", Number(4.0), Number(2.0)))
    assert evaluate(tree) == Fraction(11)


def test_evaluate_division_is_exact():
    # 1 / 4 stays an exact Fraction, not a float approximation
    result = evaluate(BinaryOp("/", Number(1.0), Number(4.0)))
    assert result == Fraction(1, 4)


def test_evaluate_division_by_zero_raises():
    with pytest.raises(UndefinedOperationError):
        evaluate(BinaryOp("/", Number(1.0), Number(0.0)))


def test_evaluate_rejects_decimal_literal():
    with pytest.raises(InvalidOperandError):
        evaluate(Number(3.14))


def test_evaluate_rejects_invalid_node():
    with pytest.raises(InvalidOperandError):
        evaluate("not a node")


def test_evaluate_rejects_unknown_operator():
    with pytest.raises(InvalidOperandError):
        evaluate(BinaryOp("%", Number(1.0), Number(2.0)))


# --- evaluate_string(): full pipeline ---

def test_full_pipeline_simple():
    assert evaluate_string("3 + 4") == Fraction(7)


def test_full_pipeline_precedence():
    assert evaluate_string("3 + 4 * 2") == Fraction(11)


def test_full_pipeline_exact_fraction_result():
    # 1 / 3 stays exact — this is the whole point of this change
    result = evaluate_string("1 / 3")
    assert result == Fraction(1, 3)


def test_full_pipeline_repeated_division_stays_exact():
    # (1/3) survives further arithmetic without float drift
    result = evaluate_string("1 / 3 + 1 / 3 + 1 / 3")
    assert result == Fraction(1)  # exactly 1, not 0.9999999999999998


def test_full_pipeline_parentheses():
    assert evaluate_string("(3 + 4) * 2") == Fraction(14)


def test_full_pipeline_unary_minus():
    assert evaluate_string("-5 + 3") == Fraction(-2)


def test_full_pipeline_decimal_literal_raises():
    with pytest.raises(InvalidOperandError):
        evaluate_string("3.14 + 1")


def test_full_pipeline_division_by_zero_raises():
    with pytest.raises(UndefinedOperationError):
        evaluate_string("1 / 0")
"""
mathforge/parser/tests/test_evaluator.py

Unit tests for the Evaluator.
"""

import pytest

from mathforge.parser.evaluator import evaluate, evaluate_string
from mathforge.parser.ast_nodes import Number, BinaryOp
from mathforge.core.errors import UndefinedOperationError, InvalidOperandError, ParserError


# --- evaluate() on hand-built trees ---

def test_evaluate_number():
    assert evaluate(Number(5.0)) == 5.0


def test_evaluate_simple_add():
    assert evaluate(BinaryOp("+", Number(3.0), Number(4.0))) == 7.0


def test_evaluate_nested():
    # 3 + (4 * 2)
    tree = BinaryOp("+", Number(3.0), BinaryOp("*", Number(4.0), Number(2.0)))
    assert evaluate(tree) == 11.0


def test_evaluate_division():
    assert evaluate(BinaryOp("/", Number(10.0), Number(4.0))) == 2.5


def test_evaluate_division_by_zero_raises():
    with pytest.raises(UndefinedOperationError):
        evaluate(BinaryOp("/", Number(1.0), Number(0.0)))


def test_evaluate_rejects_invalid_node():
    with pytest.raises(InvalidOperandError):
        evaluate("not a node")


def test_evaluate_rejects_unknown_operator():
    with pytest.raises(InvalidOperandError):
        evaluate(BinaryOp("%", Number(1.0), Number(2.0)))


# --- evaluate_string(): full pipeline, string in, number out ---

def test_full_pipeline_simple():
    assert evaluate_string("3 + 4") == 7.0


def test_full_pipeline_precedence():
    assert evaluate_string("3 + 4 * 2") == 11.0


def test_full_pipeline_precedence_division():
    assert evaluate_string("10 - 6 / 2") == 7.0


def test_full_pipeline_parentheses():
    assert evaluate_string("(3 + 4) * 2") == 14.0


def test_full_pipeline_left_associativity():
    assert evaluate_string("10 - 3 - 2") == 5.0


def test_full_pipeline_unary_minus():
    assert evaluate_string("-5 + 3") == -2.0


def test_full_pipeline_nested_parens():
    assert evaluate_string("2 * (3 + (4 - 1))") == 12.0


def test_full_pipeline_division_by_zero_raises():
    with pytest.raises(UndefinedOperationError):
        evaluate_string("1 / 0")


def test_full_pipeline_malformed_input_raises():
    with pytest.raises(ParserError):
        evaluate_string("3 + )")
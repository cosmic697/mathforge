"""
mathforge/tests/test_main.py

Unit tests for the CLI entry point.
"""

import pytest

from mathforge.__main__ import format_result, run_expression
from mathforge.arithmetic.numbers.fraction import Fraction


# --- format_result ---

def test_format_whole_number():
    assert format_result(Fraction(7)) == "7"


def test_format_negative_whole_number():
    assert format_result(Fraction(-3)) == "-3"


def test_format_fraction():
    assert format_result(Fraction(1, 3)) == "1/3"


def test_format_negative_fraction():
    assert format_result(Fraction(-1, 3)) == "-1/3"


# --- run_expression (capsys captures printed output) ---

def test_run_expression_prints_result(capsys):
    exit_code = run_expression("1 + 2")
    captured = capsys.readouterr()
    assert captured.out.strip() == "3"
    assert exit_code == 0


def test_run_expression_prints_exact_fraction(capsys):
    exit_code = run_expression("1 / 3")
    captured = capsys.readouterr()
    assert captured.out.strip() == "1/3"
    assert exit_code == 0


def test_run_expression_repeated_division_stays_exact(capsys):
    exit_code = run_expression("1 / 3 + 1 / 3 + 1 / 3")
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"
    assert exit_code == 0


def test_run_expression_handles_division_by_zero(capsys):
    exit_code = run_expression("1 / 0")
    captured = capsys.readouterr()
    assert "Error" in captured.err
    assert exit_code == 1


def test_run_expression_handles_malformed_input(capsys):
    exit_code = run_expression("3 + )")
    captured = capsys.readouterr()
    assert "Error" in captured.err
    assert exit_code == 1
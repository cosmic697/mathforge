"""
mathforge/arithmetic/tests/test_percentage.py

Unit tests for the Percentage class.
"""

import pytest

from mathforge.arithmetic.numbers.percentage import Percentage
from mathforge.arithmetic.numbers.fraction import Fraction
from mathforge.core.errors import InvalidOperandError


# --- Construction ---

def test_construct_from_fraction():
    p = Percentage(Fraction(1, 2))
    assert p.ratio == Fraction(1, 2)


def test_construct_rejects_non_fraction():
    with pytest.raises(InvalidOperandError):
        Percentage(0.5)


def test_from_percent_int():
    p = Percentage.from_percent(50)
    assert p.ratio == Fraction(1, 2)


def test_from_percent_fraction():
    p = Percentage.from_percent(Fraction(100, 3))
    assert p.ratio == Fraction(1, 3)


def test_from_percent_rejects_bool():
    with pytest.raises(InvalidOperandError):
        Percentage.from_percent(True)


def test_from_percent_rejects_invalid_type():
    with pytest.raises(InvalidOperandError):
        Percentage.from_percent("50")


# --- to_percent ---

def test_to_percent():
    p = Percentage.from_percent(50)
    assert p.to_percent() == Fraction(50, 1)


def test_to_percent_roundtrip():
    p = Percentage.from_percent(75)
    assert p.to_percent() == Fraction(75, 1)


# --- apply_to ---

def test_apply_to():
    p = Percentage.from_percent(20)
    assert p.apply_to(Fraction(50, 1)) == Fraction(10, 1)


def test_apply_to_hundred_percent():
    p = Percentage.from_percent(100)
    assert p.apply_to(Fraction(7, 1)) == Fraction(7, 1)


def test_apply_to_zero_percent():
    p = Percentage.from_percent(0)
    assert p.apply_to(Fraction(7, 1)) == Fraction(0, 1)


def test_apply_to_rejects_non_fraction():
    p = Percentage.from_percent(20)
    with pytest.raises(InvalidOperandError):
        p.apply_to(5)


# --- String representation ---

def test_str_whole_percent():
    assert str(Percentage.from_percent(50)) == "50%"


def test_str_repeating_percent():
    p = Percentage.from_percent(Fraction(100, 3))
    assert str(p) == "33.33%"


def test_repr():
    assert repr(Percentage.from_percent(50)) == "Percentage(1/2)"


# --- Arithmetic ---

def test_add():
    a = Percentage.from_percent(20)
    b = Percentage.from_percent(30)
    assert (a + b) == Percentage.from_percent(50)


def test_add_rejects_non_percentage():
    with pytest.raises(InvalidOperandError):
        Percentage.from_percent(20) + 5


def test_sub():
    a = Percentage.from_percent(50)
    b = Percentage.from_percent(20)
    assert (a - b) == Percentage.from_percent(30)


def test_sub_rejects_non_percentage():
    with pytest.raises(InvalidOperandError):
        Percentage.from_percent(50) - 5


# --- Equality / hashing ---

def test_eq_true():
    assert Percentage.from_percent(50) == Percentage(Fraction(1, 2))


def test_eq_false():
    assert Percentage.from_percent(50) != Percentage.from_percent(60)


def test_eq_non_percentage_returns_not_implemented():
    assert (Percentage.from_percent(50) == "50%") is False


def test_hashable_in_set():
    s = {Percentage.from_percent(50), Percentage(Fraction(1, 2)), Percentage.from_percent(20)}
    assert len(s) == 2
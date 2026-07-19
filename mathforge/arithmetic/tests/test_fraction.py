"""
mathforge/arithmetic/tests/test_fraction.py

Unit tests for the Fraction class.
"""

import pytest

from mathforge.arithmetic.numbers.fraction import Fraction
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError
from mathforge.core.constants import EPSILON


# --- Construction ---

def test_construction_simplifies():
    f = Fraction(2, 4)
    assert f.numerator == 1
    assert f.denominator == 2


def test_construction_already_simplified():
    f = Fraction(3, 5)
    assert f.numerator == 3
    assert f.denominator == 5


def test_negative_denominator_normalizes_sign():
    f = Fraction(1, -2)
    assert f.numerator == -1
    assert f.denominator == 2


def test_both_negative_becomes_positive():
    f = Fraction(-1, -2)
    assert f.numerator == 1
    assert f.denominator == 2


def test_default_denominator_is_one():
    f = Fraction(5)
    assert f.numerator == 5
    assert f.denominator == 1


def test_zero_numerator():
    f = Fraction(0, 5)
    assert f.numerator == 0
    assert f.denominator == 1


def test_zero_denominator_raises():
    with pytest.raises(UndefinedOperationError):
        Fraction(1, 0)


@pytest.mark.parametrize("num, den", [
    (1.5, 2),
    ("1", 2),
    (None, 2),
    (1, 2.0),
    (True, 2),
    (1, False),
])
def test_invalid_types_raise(num, den):
    with pytest.raises(InvalidOperandError):
        Fraction(num, den)


# --- String representation ---

def test_str():
    assert str(Fraction(3, 4)) == "3/4"


def test_repr():
    assert repr(Fraction(3, 4)) == "Fraction(3, 4)"


# --- Arithmetic ---

def test_add():
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)


def test_add_rejects_non_fraction():
    with pytest.raises(InvalidOperandError):
        Fraction(1, 2) + 3


def test_sub():
    assert Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6)


def test_sub_rejects_non_fraction():
    with pytest.raises(InvalidOperandError):
        Fraction(1, 2) - 3


def test_mul():
    assert Fraction(2, 3) * Fraction(3, 4) == Fraction(1, 2)


def test_mul_rejects_non_fraction():
    with pytest.raises(InvalidOperandError):
        Fraction(1, 2) * 3


def test_truediv():
    assert Fraction(1, 2) / Fraction(1, 3) == Fraction(3, 2)


def test_truediv_by_zero_raises():
    with pytest.raises(UndefinedOperationError):
        Fraction(1, 2) / Fraction(0, 1)


def test_truediv_rejects_non_fraction():
    with pytest.raises(InvalidOperandError):
        Fraction(1, 2) / 3


# --- Equality and hashing ---

def test_eq_true():
    assert Fraction(1, 2) == Fraction(2, 4)


def test_eq_false():
    assert Fraction(1, 2) != Fraction(1, 3)


def test_eq_non_fraction_returns_not_implemented():
    assert (Fraction(1, 2) == "1/2") is False


def test_hash_consistent_with_eq():
    assert hash(Fraction(1, 2)) == hash(Fraction(2, 4))


def test_hashable_in_set():
    s = {Fraction(1, 2), Fraction(2, 4), Fraction(1, 3)}
    assert len(s) == 2  # first two are equal, so they collapse


# --- reciprocal ---

def test_reciprocal():
    assert Fraction(2, 3).reciprocal() == Fraction(3, 2)


def test_reciprocal_of_negative():
    assert Fraction(-2, 3).reciprocal() == Fraction(-3, 2)


def test_reciprocal_of_zero_raises():
    with pytest.raises(UndefinedOperationError):
        Fraction(0, 1).reciprocal()


# --- to_float ---

def test_to_float():
    assert abs(Fraction(1, 2).to_float() - 0.5) < EPSILON


def test_to_float_negative():
    assert abs(Fraction(-3, 4).to_float() - (-0.75)) < EPSILON


# --- __neg__ ---

def test_neg():
    assert -Fraction(1, 2) == Fraction(-1, 2)


def test_neg_of_negative():
    assert -Fraction(-1, 2) == Fraction(1, 2)


# --- __abs__ ---

def test_abs_of_positive():
    assert abs(Fraction(3, 4)) == Fraction(3, 4)


def test_abs_of_negative():
    assert abs(Fraction(-3, 4)) == Fraction(3, 4)


def test_abs_of_zero():
    assert abs(Fraction(0, 1)) == Fraction(0, 1)
"""
mathforge/arithmetic/tests/test_decimal.py

Unit tests for the Decimal class.
"""

import pytest

from mathforge.arithmetic.numbers.decimal import Decimal
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError


# --- Construction ---

def test_construct_from_string():
    d = Decimal("3.14")
    assert str(d) == "3.14"


def test_construct_from_negative_string():
    d = Decimal("-0.5")
    assert str(d) == "-0.5"


def test_construct_from_int_string_no_decimal_point():
    d = Decimal("10")
    assert str(d) == "10"


def test_construct_from_int():
    d = Decimal(7)
    assert str(d) == "7"


def test_construct_with_leading_zero_fraction():
    d = Decimal("0.05")
    assert str(d) == "0.05"


def test_construct_rejects_float():
    with pytest.raises(InvalidOperandError):
        Decimal(3.14)


def test_construct_rejects_bool():
    with pytest.raises(InvalidOperandError):
        Decimal(True)


@pytest.mark.parametrize("bad", ["abc", "1.2.3", "", "--1"])
def test_construct_rejects_invalid_string(bad):
    with pytest.raises(InvalidOperandError):
        Decimal(bad)


# --- String / repr ---

def test_repr():
    assert repr(Decimal("3.14")) == "Decimal('3.14')"


# --- Equality (exponent-aligned) ---

def test_eq_same_value_different_exponents():
    assert Decimal("1.50") == Decimal("1.5")


def test_eq_false():
    assert Decimal("1.5") != Decimal("1.6")


def test_unhashable():
    with pytest.raises(TypeError):
        hash(Decimal("1.5"))


# --- Arithmetic ---

def test_add_different_exponents():
    assert Decimal("1.1") + Decimal("2.22") == Decimal("3.32")


def test_add_rejects_non_decimal():
    with pytest.raises(InvalidOperandError):
        Decimal("1.5") + 3


def test_sub():
    assert Decimal("5.5") - Decimal("2.2") == Decimal("3.3")


def test_sub_rejects_non_decimal():
    with pytest.raises(InvalidOperandError):
        Decimal("1.5") - 3


def test_mul():
    assert Decimal("2.5") * Decimal("4") == Decimal("10")


def test_mul_rejects_non_decimal():
    with pytest.raises(InvalidOperandError):
        Decimal("1.5") * 3


def test_truediv_exact():
    assert Decimal("1") / Decimal("4") == Decimal("0.25")


def test_truediv_rounds_repeating_decimal():
    result = Decimal("1") / Decimal("3")
    assert abs(result.to_float() - (1 / 3)) < 1e-9


def test_truediv_by_zero_raises():
    with pytest.raises(UndefinedOperationError):
        Decimal("1") / Decimal("0")


def test_truediv_rejects_non_decimal():
    with pytest.raises(InvalidOperandError):
        Decimal("1.5") / 3


# --- to_float ---

def test_to_float():
    assert abs(Decimal("3.14").to_float() - 3.14) < 1e-9


# --- neg / abs ---

def test_neg():
    assert -Decimal("3.14") == Decimal("-3.14")


def test_abs_of_negative():
    assert abs(Decimal("-3.14")) == Decimal("3.14")


def test_abs_of_positive():
    assert abs(Decimal("3.14")) == Decimal("3.14")
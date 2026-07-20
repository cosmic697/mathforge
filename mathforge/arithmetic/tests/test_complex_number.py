"""
mathforge/arithmetic/tests/test_complex_number.py

Unit tests for the ComplexNumber class.
"""

import pytest

from mathforge.arithmetic.numbers.complex_numbers import ComplexNumber
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError
from mathforge.core.constants import EPSILON


# --- Construction ---

def test_construction_basic():
    c = ComplexNumber(3, 4)
    assert c.real == 3.0
    assert c.imag == 4.0


def test_default_imag_is_zero():
    c = ComplexNumber(5)
    assert c.real == 5.0
    assert c.imag == 0.0


def test_construction_stores_as_float():
    c = ComplexNumber(3, 4)
    assert isinstance(c.real, float)
    assert isinstance(c.imag, float)


def test_construction_accepts_float_input():
    c = ComplexNumber(1.5, -2.5)
    assert c.real == 1.5
    assert c.imag == -2.5


@pytest.mark.parametrize("real, imag", [
    ("3", 4),
    (3, "4"),
    (None, 4),
    (True, 4),
    (3, False),
])
def test_invalid_types_raise(real, imag):
    with pytest.raises(InvalidOperandError):
        ComplexNumber(real, imag)


# --- String representation ---

def test_str_positive_imag():
    assert str(ComplexNumber(3, 4)) == "3.0 + 4.0i"


def test_str_negative_imag():
    assert str(ComplexNumber(3, -4)) == "3.0 - 4.0i"


def test_repr():
    assert repr(ComplexNumber(3, 4)) == "ComplexNumber(3.0, 4.0)"


# --- Arithmetic ---

def test_add():
    assert ComplexNumber(1, 2) + ComplexNumber(3, -1) == ComplexNumber(4, 1)


def test_add_rejects_non_complex():
    with pytest.raises(InvalidOperandError):
        ComplexNumber(1, 2) + 3


def test_sub():
    assert ComplexNumber(5, 3) - ComplexNumber(2, 1) == ComplexNumber(3, 2)


def test_sub_rejects_non_complex():
    with pytest.raises(InvalidOperandError):
        ComplexNumber(1, 2) - 3


def test_mul():
    assert ComplexNumber(1, 2) * ComplexNumber(3, 4) == ComplexNumber(-5, 10)


def test_mul_rejects_non_complex():
    with pytest.raises(InvalidOperandError):
        ComplexNumber(1, 2) * 3


def test_truediv():
    result = ComplexNumber(1, 2) / ComplexNumber(1, -2)
    assert result == ComplexNumber(-0.6, 0.8)


def test_truediv_by_zero_raises():
    with pytest.raises(UndefinedOperationError):
        ComplexNumber(1, 2) / ComplexNumber(0, 0)


def test_truediv_rejects_non_complex():
    with pytest.raises(InvalidOperandError):
        ComplexNumber(1, 2) / 3


# --- Equality (tolerance-based) ---

def test_eq_true():
    assert ComplexNumber(1, 2) == ComplexNumber(1, 2)


def test_eq_false():
    assert ComplexNumber(1, 2) != ComplexNumber(1, 3)


def test_eq_within_epsilon():
    assert ComplexNumber(1, 2) == ComplexNumber(1 + EPSILON / 10, 2)


def test_eq_non_complex_returns_false():
    assert (ComplexNumber(1, 2) == "1+2i") is False


def test_unhashable():
    with pytest.raises(TypeError):
        hash(ComplexNumber(1, 2))


# --- conjugate ---

def test_conjugate():
    assert ComplexNumber(3, 4).conjugate() == ComplexNumber(3, -4)


def test_conjugate_of_real():
    assert ComplexNumber(5, 0).conjugate() == ComplexNumber(5, 0)


# --- magnitude ---

def test_magnitude():
    assert abs(ComplexNumber(3, 4).magnitude() - 5.0) < EPSILON


def test_magnitude_of_zero():
    assert ComplexNumber(0, 0).magnitude() == 0.0


# --- __neg__ ---

def test_neg():
    assert -ComplexNumber(3, 4) == ComplexNumber(-3, -4)


# --- __abs__ ---

def test_abs_returns_float():
    result = abs(ComplexNumber(3, 4))
    assert isinstance(result, float)
    assert abs(result - 5.0) < EPSILON
"""
mathforge/linear_algebra/tests/test_vector.py

Unit tests for the Vector class.
"""

import pytest

from mathforge.linear_algebra.vector import Vector
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError


# --- Construction ---

def test_construct_basic():
    v = Vector([1, 2, 3])
    assert v.components == (1.0, 2.0, 3.0)


def test_construct_converts_to_float():
    v = Vector([1, 2, 3])
    assert all(isinstance(c, float) for c in v.components)


def test_construct_single_dimension():
    v = Vector([5])
    assert v.dimension == 1


def test_construct_empty_raises():
    with pytest.raises(InvalidOperandError):
        Vector([])


def test_construct_rejects_string():
    with pytest.raises(InvalidOperandError):
        Vector("123")


def test_construct_rejects_bool_component():
    with pytest.raises(InvalidOperandError):
        Vector([1, True, 3])


def test_construct_rejects_non_numeric_component():
    with pytest.raises(InvalidOperandError):
        Vector([1, "2", 3])


# --- dimension / len / indexing ---

def test_dimension():
    assert Vector([1, 2, 3, 4]).dimension == 4


def test_len():
    assert len(Vector([1, 2, 3])) == 3


def test_getitem():
    v = Vector([10, 20, 30])
    assert v[0] == 10.0
    assert v[2] == 30.0


def test_getitem_out_of_range_raises_index_error():
    v = Vector([1, 2])
    with pytest.raises(IndexError):
        v[5]


# --- String representation ---

def test_str():
    assert str(Vector([1, 2, 3])) == "(1.0, 2.0, 3.0)"


def test_repr():
    assert repr(Vector([1, 2, 3])) == "Vector(1.0, 2.0, 3.0)"


# --- Equality ---

def test_eq_true():
    assert Vector([1, 2, 3]) == Vector([1, 2, 3])


def test_eq_false_different_values():
    assert Vector([1, 2, 3]) != Vector([1, 2, 4])


def test_eq_false_different_dimension():
    assert Vector([1, 2]) != Vector([1, 2, 3])


def test_eq_non_vector_returns_false():
    assert (Vector([1, 2]) == [1, 2]) is False


# --- Arithmetic ---

def test_add():
    assert Vector([1, 0, 0]) + Vector([0, 1, 0]) == Vector([1, 1, 0])


def test_add_rejects_non_vector():
    with pytest.raises(InvalidOperandError):
        Vector([1, 2]) + 5


def test_add_rejects_mismatched_dimension():
    with pytest.raises(InvalidOperandError):
        Vector([1, 2]) + Vector([1, 2, 3])


def test_sub():
    assert Vector([5, 5]) - Vector([2, 1]) == Vector([3, 4])


def test_sub_rejects_mismatched_dimension():
    with pytest.raises(InvalidOperandError):
        Vector([1, 2]) - Vector([1, 2, 3])


def test_mul_scalar():
    assert Vector([1, 2, 3]) * 2 == Vector([2, 4, 6])


def test_rmul_scalar():
    assert 2 * Vector([1, 2, 3]) == Vector([2, 4, 6])


def test_mul_rejects_non_scalar():
    with pytest.raises(InvalidOperandError):
        Vector([1, 2]) * Vector([1, 2])


def test_mul_rejects_bool():
    with pytest.raises(InvalidOperandError):
        Vector([1, 2]) * True


# --- dot product ---

def test_dot():
    assert Vector([1, 2, 3]).dot(Vector([4, 5, 6])) == 32.0


def test_dot_orthogonal_vectors():
    assert Vector([1, 0]).dot(Vector([0, 1])) == 0.0


def test_dot_rejects_mismatched_dimension():
    with pytest.raises(InvalidOperandError):
        Vector([1, 2]).dot(Vector([1, 2, 3]))


def test_dot_rejects_non_vector():
    with pytest.raises(InvalidOperandError):
        Vector([1, 2]).dot(5)


# --- cross product ---

def test_cross_standard_basis():
    # i x j = k
    assert Vector([1, 0, 0]).cross(Vector([0, 1, 0])) == Vector([0, 0, 1])


def test_cross_rejects_non_3d():
    with pytest.raises(UndefinedOperationError):
        Vector([1, 2]).cross(Vector([3, 4]))


def test_cross_rejects_non_vector():
    with pytest.raises(InvalidOperandError):
        Vector([1, 2, 3]).cross(5)


# --- magnitude ---

def test_magnitude():
    assert Vector([3, 4]).magnitude() == 5.0


def test_magnitude_of_zero_vector():
    assert Vector([0, 0, 0]).magnitude() == 0.0


# --- normalize ---

def test_normalize():
    result = Vector([3, 4]).normalize()
    assert abs(result.magnitude() - 1.0) < 1e-9


def test_normalize_zero_vector_raises():
    with pytest.raises(UndefinedOperationError):
        Vector([0, 0]).normalize()


# --- neg ---

def test_neg():
    assert -Vector([1, -2, 3]) == Vector([-1, 2, -3])
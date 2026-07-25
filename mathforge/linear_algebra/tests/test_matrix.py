"""
mathforge/linear_algebra/tests/test_matrix.py

Unit tests for the Matrix class.
"""

import pytest

from mathforge.linear_algebra.matrix import Matrix
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError


# --- Construction ---

def test_construct_basic():
    m = Matrix([[1, 2], [3, 4]])
    assert m.shape == (2, 2)
    assert m[0, 0] == 1.0
    assert m[1, 1] == 4.0


def test_construct_converts_to_float():
    m = Matrix([[1, 2], [3, 4]])
    assert all(isinstance(x, float) for row in m._data for x in row)


def test_construct_non_square():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m.shape == (2, 3)


def test_construct_empty_raises():
    with pytest.raises(InvalidOperandError):
        Matrix([])


def test_construct_empty_row_raises():
    with pytest.raises(InvalidOperandError):
        Matrix([[]])


def test_construct_inconsistent_row_length_raises():
    with pytest.raises(InvalidOperandError):
        Matrix([[1, 2], [3, 4, 5]])


def test_construct_rejects_bool_element():
    with pytest.raises(InvalidOperandError):
        Matrix([[1, True], [3, 4]])


def test_construct_rejects_non_numeric_element():
    with pytest.raises(InvalidOperandError):
        Matrix([[1, "2"], [3, 4]])


# --- Factory methods ---

def test_identity():
    m = Matrix.identity(3)
    assert m == Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


def test_identity_rejects_non_positive():
    with pytest.raises(InvalidOperandError):
        Matrix.identity(0)


def test_zero_factory():
    m = Matrix.zero(2, 3)
    assert m == Matrix([[0, 0, 0], [0, 0, 0]])


# --- Shape / indexing ---

def test_rows_cols_shape():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m.rows == 2
    assert m.cols == 3
    assert m.shape == (2, 3)


def test_is_square():
    assert Matrix([[1, 2], [3, 4]]).is_square is True
    assert Matrix([[1, 2, 3], [4, 5, 6]]).is_square is False


def test_getitem_row():
    m = Matrix([[1, 2], [3, 4]])
    assert m[0] == (1.0, 2.0)


def test_getitem_element():
    m = Matrix([[1, 2], [3, 4]])
    assert m[1, 0] == 3.0


def test_getitem_out_of_range_raises_index_error():
    m = Matrix([[1, 2], [3, 4]])
    with pytest.raises(IndexError):
        m[5]


# --- String representation ---

def test_repr():
    assert repr(Matrix([[1, 2], [3, 4]])) == "Matrix([1.0, 2.0], [3.0, 4.0])"


def test_str():
    assert str(Matrix([[1, 2], [3, 4]])) == "1.0 2.0\n3.0 4.0"


# --- Equality ---

def test_eq_true():
    assert Matrix([[1, 2], [3, 4]]) == Matrix([[1, 2], [3, 4]])


def test_eq_false_different_values():
    assert Matrix([[1, 2], [3, 4]]) != Matrix([[1, 2], [3, 5]])


def test_eq_false_different_shape():
    assert Matrix([[1, 2]]) != Matrix([[1, 2], [3, 4]])


def test_eq_non_matrix_returns_false():
    assert (Matrix([[1, 2]]) == [[1, 2]]) is False


# --- Add / Subtract ---

def test_add():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    assert (a + b) == Matrix([[6, 8], [10, 12]])


def test_add_rejects_non_matrix():
    with pytest.raises(InvalidOperandError):
        Matrix([[1, 2]]) + 5


def test_add_rejects_mismatched_shape():
    with pytest.raises(InvalidOperandError):
        Matrix([[1, 2]]) + Matrix([[1, 2], [3, 4]])


def test_sub():
    a = Matrix([[5, 6], [7, 8]])
    b = Matrix([[1, 2], [3, 4]])
    assert (a - b) == Matrix([[4, 4], [4, 4]])


def test_sub_rejects_mismatched_shape():
    with pytest.raises(InvalidOperandError):
        Matrix([[1, 2]]) - Matrix([[1, 2], [3, 4]])


# --- Scalar multiplication ---

def test_mul_scalar():
    m = Matrix([[1, 2], [3, 4]])
    assert (m * 2) == Matrix([[2, 4], [6, 8]])


def test_rmul_scalar():
    m = Matrix([[1, 2], [3, 4]])
    assert (2 * m) == Matrix([[2, 4], [6, 8]])


def test_mul_rejects_bool_scalar():
    with pytest.raises(InvalidOperandError):
        Matrix([[1, 2]]) * True


# --- Matrix multiplication ---

def test_mul_matrix():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    # [1*5+2*7, 1*6+2*8] = [19, 22]
    # [3*5+4*7, 3*6+4*8] = [43, 50]
    assert (a * b) == Matrix([[19, 22], [43, 50]])


def test_mul_matrix_non_square_shapes():
    a = Matrix([[1, 2, 3]])          # 1x3
    b = Matrix([[1], [1], [1]])      # 3x1
    assert (a * b) == Matrix([[6]])  # 1x1


def test_mul_matrix_rejects_mismatched_inner_dimension():
    a = Matrix([[1, 2]])       # 1x2
    b = Matrix([[1, 2]])       # 1x2 — inner dims 2 != 1, invalid
    with pytest.raises(InvalidOperandError):
        a * b


# --- Transpose ---

def test_transpose():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m.transpose() == Matrix([[1, 4], [2, 5], [3, 6]])


def test_transpose_square():
    m = Matrix([[1, 2], [3, 4]])
    assert m.transpose() == Matrix([[1, 3], [2, 4]])


# --- Determinant ---

def test_determinant_2x2():
    m = Matrix([[4, 6], [3, 8]])
    assert abs(m.determinant() - 14.0) < 1e-9


def test_determinant_identity():
    assert abs(Matrix.identity(3).determinant() - 1.0) < 1e-9


def test_determinant_singular_is_zero():
    m = Matrix([[1, 2], [2, 4]])  # row 2 = 2 * row 1
    assert abs(m.determinant() - 0.0) < 1e-9


def test_determinant_3x3():
    m = Matrix([[6, 1, 1], [4, -2, 5], [2, 8, 7]])
    # known determinant = -306
    assert abs(m.determinant() - (-306.0)) < 1e-6


def test_determinant_rejects_non_square():
    with pytest.raises(UndefinedOperationError):
        Matrix([[1, 2, 3], [4, 5, 6]]).determinant()


# --- Inverse ---

def test_inverse_2x2():
    m = Matrix([[4, 7], [2, 6]])
    inv = m.inverse()
    assert (m * inv) == Matrix.identity(2)


def test_inverse_identity_is_identity():
    assert Matrix.identity(3).inverse() == Matrix.identity(3)


def test_inverse_singular_raises():
    m = Matrix([[1, 2], [2, 4]])
    with pytest.raises(UndefinedOperationError):
        m.inverse()


def test_inverse_rejects_non_square():
    with pytest.raises(UndefinedOperationError):
        Matrix([[1, 2, 3], [4, 5, 6]]).inverse()


# --- Negation ---

def test_neg():
    m = Matrix([[1, -2], [3, -4]])
    assert -m == Matrix([[-1, 2], [-3, 4]])
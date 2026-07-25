"""
mathforge/linear_algebra/matrix.py

Matrix

Represents a 2D matrix of floats, with element-wise arithmetic,
matrix multiplication, transpose, determinant, and inverse.
"""

from mathforge.core.errors import InvalidOperandError, UndefinedOperationError
from mathforge.core.constants import EPSILON


class Matrix:
    """
    A 2D matrix of floats.

    Internally stored as a tuple of tuples (rows), reinforcing
    immutability — every operation returns a new Matrix rather
    than modifying self.

    Attributes
    ----------
    rows : int
        Number of rows.
    cols : int
        Number of columns.
    shape : tuple of (int, int)
        (rows, cols).

    Examples
    --------
    >>> Matrix([[1, 2], [3, 4]])
    Matrix([1.0, 2.0], [3.0, 4.0])
    >>> Matrix.identity(2)
    Matrix([1.0, 0.0], [0.0, 1.0])
    """

    def __init__(self, data):
        """
        Construct a Matrix from a sequence of rows.

        Parameters
        ----------
        data : sequence of sequences of int/float
            Each inner sequence is a row. All rows must have the
            same length. Elements are converted to float.

        Raises
        ------
        InvalidOperandError
            If data is empty, rows have inconsistent lengths, a
            row is empty, or any element is not int/float (or is
            a bool).
        """
        try:
            row_list = list(data)
        except TypeError:
            raise InvalidOperandError("data must be a sequence of rows.")

        if len(row_list) == 0:
            raise InvalidOperandError("Matrix must have at least one row.")

        converted_rows = []
        row_length = None
        for row in row_list:
            try:
                items = list(row)
            except TypeError:
                raise InvalidOperandError("each row must be a sequence of numbers.")

            if len(items) == 0:
                raise InvalidOperandError("rows must not be empty.")

            if row_length is None:
                row_length = len(items)
            elif len(items) != row_length:
                raise InvalidOperandError("all rows must have the same length.")

            converted = []
            for item in items:
                if isinstance(item, bool):
                    raise InvalidOperandError("elements must be numbers, not booleans.")
                if not isinstance(item, (int, float)):
                    raise InvalidOperandError("elements must be int or float.")
                converted.append(float(item))

            converted_rows.append(tuple(converted))

        self._data = tuple(converted_rows)

    @classmethod
    def identity(cls, n: int) -> "Matrix":
        """
        Construct an n x n identity matrix.

        Parameters
        ----------
        n : int
            Must be a positive integer.

        Returns
        -------
        Matrix

        Raises
        ------
        InvalidOperandError
            If n is not a positive int.
        """
        if isinstance(n, bool) or not isinstance(n, int):
            raise InvalidOperandError("n must be an int.")
        if n <= 0:
            raise InvalidOperandError("n must be positive.")
        return cls([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])

    @classmethod
    def zero(cls, rows: int, cols: int) -> "Matrix":
        """
        Construct a rows x cols matrix of zeros.

        Parameters
        ----------
        rows : int
        cols : int

        Returns
        -------
        Matrix

        Raises
        ------
        InvalidOperandError
            If rows or cols is not a positive int.
        """
        if isinstance(rows, bool) or not isinstance(rows, int) or rows <= 0:
            raise InvalidOperandError("rows must be a positive int.")
        if isinstance(cols, bool) or not isinstance(cols, int) or cols <= 0:
            raise InvalidOperandError("cols must be a positive int.")
        return cls([[0.0] * cols for _ in range(rows)])

    @property
    def rows(self) -> int:
        """int: Number of rows."""
        return len(self._data)

    @property
    def cols(self) -> int:
        """int: Number of columns."""
        return len(self._data[0])

    @property
    def shape(self) -> tuple:
        """tuple of (int, int): (rows, cols)."""
        return (self.rows, self.cols)

    @property
    def is_square(self) -> bool:
        """bool: True if rows == cols."""
        return self.rows == self.cols

    def __getitem__(self, key):
        """
        Access a row or a single element.

        Parameters
        ----------
        key : int or tuple of (int, int)
            matrix[i] returns row i as a tuple.
            matrix[i, j] returns the element at row i, column j.

        Returns
        -------
        tuple or float

        Raises
        ------
        IndexError
            If the index is out of range (standard Python behavior).
        """
        if isinstance(key, tuple):
            i, j = key
            return self._data[i][j]
        return self._data[key]

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            In the form "Matrix([1.0, 2.0], [3.0, 4.0])".
        """
        rows_str = ", ".join(f"[{', '.join(str(x) for x in row)}]" for row in self._data)
        return f"Matrix({rows_str})"

    def __str__(self) -> str:
        """
        Returns
        -------
        str
            Each row on its own line, e.g.:
            "1.0 2.0\\n3.0 4.0"
        """
        return "\n".join(" ".join(str(x) for x in row) for row in self._data)

    def __eq__(self, other: object) -> bool:
        """
        Check equality: same shape, and all elements within EPSILON.

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            NotImplemented if other is not a Matrix.
        """
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape != other.shape:
            return False
        for row_a, row_b in zip(self._data, other._data):
            for a, b in zip(row_a, row_b):
                if abs(a - b) >= EPSILON:
                    return False
        return True

    def _check_same_shape(self, other: "Matrix", op_name: str):
        if not isinstance(other, Matrix):
            raise InvalidOperandError(f"can only {op_name} Matrix with Matrix")
        if self.shape != other.shape:
            raise InvalidOperandError(
                f"cannot {op_name} matrices of different shapes "
                f"({self.shape} vs {other.shape})"
            )

    def __add__(self, other: "Matrix") -> "Matrix":
        """
        Add two matrices element-wise. Requires equal shape.

        Parameters
        ----------
        other : Matrix

        Returns
        -------
        Matrix

        Raises
        ------
        InvalidOperandError
            If other is not a Matrix, or shapes don't match.
        """
        self._check_same_shape(other, "add")
        return Matrix([
            [a + b for a, b in zip(row_a, row_b)]
            for row_a, row_b in zip(self._data, other._data)
        ])

    def __sub__(self, other: "Matrix") -> "Matrix":
        """
        Subtract two matrices element-wise. Requires equal shape.

        Parameters
        ----------
        other : Matrix

        Returns
        -------
        Matrix

        Raises
        ------
        InvalidOperandError
            If other is not a Matrix, or shapes don't match.
        """
        self._check_same_shape(other, "subtract")
        return Matrix([
            [a - b for a, b in zip(row_a, row_b)]
            for row_a, row_b in zip(self._data, other._data)
        ])

    def __mul__(self, other):
        """
        Multiply by a scalar (element-wise) or another Matrix
        (true matrix multiplication).

        For Matrix * Matrix: self must be (m x n) and other must
        be (n x p); result is (m x p). Requires self.cols == other.rows.

        Parameters
        ----------
        other : int, float, or Matrix

        Returns
        -------
        Matrix

        Raises
        ------
        InvalidOperandError
            If other is not a scalar or Matrix, or (for Matrix *
            Matrix) if inner dimensions don't match
            (self.cols != other.rows).
        """
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise InvalidOperandError(
                    f"cannot multiply {self.shape} matrix by {other.shape} matrix "
                    f"— inner dimensions must match ({self.cols} != {other.rows})"
                )
            result = [
                [
                    sum(self._data[i][k] * other._data[k][j] for k in range(self.cols))
                    for j in range(other.cols)
                ]
                for i in range(self.rows)
            ]
            return Matrix(result)

        if isinstance(other, bool) or not isinstance(other, (int, float)):
            raise InvalidOperandError("can only multiply Matrix by a scalar or another Matrix")

        return Matrix([[x * other for x in row] for row in self._data])

    def __rmul__(self, scalar):
        """
        Support scalar * matrix (reversed operand order).

        Parameters
        ----------
        scalar : int or float

        Returns
        -------
        Matrix
        """
        return self.__mul__(scalar)

    def transpose(self) -> "Matrix":
        """
        Return the transpose (rows and columns swapped).

        Returns
        -------
        Matrix
            A new (cols x rows) Matrix where element [j][i] of the
            result equals element [i][j] of self.
        """
        return Matrix([
            [self._data[i][j] for i in range(self.rows)]
            for j in range(self.cols)
        ])

    def determinant(self) -> float:
        """
        Compute the determinant via Gaussian elimination with
        partial pivoting.

        Reduces the matrix to upper-triangular form by row
        operations, tracking the sign flip from each row swap;
        the determinant is then the product of the diagonal,
        adjusted for sign. This is O(n^3), versus O(n!) for naive
        cofactor expansion — the same practical reason real
        numerical libraries don't use cofactor expansion beyond
        tiny matrices.

        Returns
        -------
        float

        Raises
        ------
        UndefinedOperationError
            If the matrix is not square.
        """
        if not self.is_square:
            raise UndefinedOperationError("determinant is only defined for square matrices")

        n = self.rows
        a = [list(row) for row in self._data]
        det = 1.0

        for col in range(n):
            pivot_row = max(range(col, n), key=lambda r: abs(a[r][col]))
            if abs(a[pivot_row][col]) < EPSILON:
                return 0.0

            if pivot_row != col:
                a[col], a[pivot_row] = a[pivot_row], a[col]
                det *= -1

            det *= a[col][col]

            for r in range(col + 1, n):
                factor = a[r][col] / a[col][col]
                for c in range(col, n):
                    a[r][c] -= factor * a[col][c]

        return det

    def inverse(self) -> "Matrix":
        """
        Compute the inverse via Gauss-Jordan elimination.

        Augments self with the identity matrix, then row-reduces
        the left half to the identity — the right half becomes
        the inverse. Uses partial pivoting for numerical stability.

        Returns
        -------
        Matrix

        Raises
        ------
        UndefinedOperationError
            If the matrix is not square, or is singular
            (determinant is effectively zero — no inverse exists).
        """
        if not self.is_square:
            raise UndefinedOperationError("inverse is only defined for square matrices")

        n = self.rows
        a = [list(row) for row in self._data]
        identity = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

        for col in range(n):
            pivot_row = max(range(col, n), key=lambda r: abs(a[r][col]))
            if abs(a[pivot_row][col]) < EPSILON:
                raise UndefinedOperationError("matrix is singular; no inverse exists")

            a[col], a[pivot_row] = a[pivot_row], a[col]
            identity[col], identity[pivot_row] = identity[pivot_row], identity[col]

            pivot = a[col][col]
            a[col] = [x / pivot for x in a[col]]
            identity[col] = [x / pivot for x in identity[col]]

            for r in range(n):
                if r != col:
                    factor = a[r][col]
                    a[r] = [a[r][c] - factor * a[col][c] for c in range(n)]
                    identity[r] = [identity[r][c] - factor * identity[col][c] for c in range(n)]

        return Matrix(identity)

    def __neg__(self) -> "Matrix":
        """
        Returns
        -------
        Matrix
            A new Matrix with every element sign-flipped.
        """
        return Matrix([[-x for x in row] for row in self._data])
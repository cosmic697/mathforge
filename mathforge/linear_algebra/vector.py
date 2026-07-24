"""
mathforge/linear_algebra/vector.py

Vector

Represents a mathematical vector as an ordered, fixed-length
sequence of float components.
"""

import math

from mathforge.core.errors import InvalidOperandError, UndefinedOperationError


class Vector:
    """
    A mathematical vector of arbitrary dimension.

    Vector instances are immutable — every operation returns a new
    Vector rather than modifying self.

    By default, operations between vectors of different dimensions
    raise InvalidOperandError — this catches accidental mismatches
    (e.g. mixing up a 2D and 3D vector). Pass pad=True to instead
    treat missing components on the shorter vector as 0, extending
    it to match the longer vector's dimension. Use pad=True only
    when a dimension mismatch is genuinely expected and meaningful
    in your context, not as a default habit — it silently hides the
    exact class of bug the strict check exists to catch.
    """

    def __init__(self, components):
        """
        Construct a Vector from a sequence of numbers.

        Parameters
        ----------
        components : sequence of int/float
            The vector's components. Must be non-empty. Each
            element is converted to float.

        Raises
        ------
        InvalidOperandError
            If components is empty, is not a sequence, or contains
            a non-numeric or boolean element.
        """
        if isinstance(components, (str, bytes)):
            raise InvalidOperandError("components must be a sequence of numbers, not a string.")

        try:
            items = list(components)
        except TypeError:
            raise InvalidOperandError("components must be an iterable sequence of numbers.")

        if len(items) == 0:
            raise InvalidOperandError("Vector must have at least one component.")

        converted = []
        for item in items:
            if isinstance(item, bool):
                raise InvalidOperandError("components must be numbers, not booleans.")
            if not isinstance(item, (int, float)):
                raise InvalidOperandError("components must be int or float.")
            converted.append(float(item))

        self._components = tuple(converted)

    @classmethod
    def zero(cls, dimension: int) -> "Vector":
        """
        Construct a zero vector of the given dimension.

        Parameters
        ----------
        dimension : int
            Must be a positive integer.

        Returns
        -------
        Vector
            A vector with `dimension` components, all 0.0.

        Raises
        ------
        InvalidOperandError
            If dimension is not a positive int.
        """
        if isinstance(dimension, bool) or not isinstance(dimension, int):
            raise InvalidOperandError("dimension must be an int.")
        if dimension <= 0:
            raise InvalidOperandError("dimension must be positive.")
        return cls([0.0] * dimension)

    @property
    def components(self) -> tuple:
        """
        tuple of float: The vector's components.
        """
        return self._components

    @property
    def dimension(self) -> int:
        """
        int: The number of components (the vector's dimension).
        """
        return len(self._components)

    def __len__(self) -> int:
        """
        Returns
        -------
        int
            Same as self.dimension.
        """
        return self.dimension

    def __getitem__(self, index: int) -> float:
        """
        Return the component at the given index.

        Parameters
        ----------
        index : int

        Returns
        -------
        float

        Raises
        ------
        IndexError
            If index is out of range (standard Python sequence
            behavior, propagated from the underlying tuple).
        """
        return self._components[index]

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            In the form "Vector(1.0, 2.0, 3.0)".
        """
        inner = ", ".join(str(c) for c in self._components)
        return f"Vector({inner})"

    def __str__(self) -> str:
        """
        Returns
        -------
        str
            In the form "(1.0, 2.0, 3.0)".
        """
        inner = ", ".join(str(c) for c in self._components)
        return f"({inner})"

    def __eq__(self, other: object) -> bool:
        """
        Check equality: same dimension and all components equal.

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            NotImplemented if other is not a Vector.
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return self._components == other._components

    def _padded_pair(self, other: "Vector", op_name: str, pad: bool):
        """
        Internal helper: validate `other` is a Vector, then return
        (self_components, other_components) as equal-length tuples.

        If dimensions already match, returns them unchanged. If they
        differ and pad=True, the shorter one is right-padded with 0.0.
        If they differ and pad=False, raises InvalidOperandError.
        """
        if not isinstance(other, Vector):
            raise InvalidOperandError(f"can only {op_name} Vector with Vector")

        a, b = self._components, other._components
        if len(a) == len(b):
            return a, b

        if not pad:
            raise InvalidOperandError(
                f"cannot {op_name} vectors of different dimensions "
                f"({len(a)} vs {len(b)}). Pass pad=True to treat "
                f"missing components as 0."
            )

        target = max(len(a), len(b))
        a = a + (0.0,) * (target - len(a))
        b = b + (0.0,) * (target - len(b))
        return a, b

    def __add__(self, other: "Vector") -> "Vector":
        """
        Add two vectors component-wise. Requires equal dimensions;
        for zero-padded addition of mismatched dimensions, use
        add(other, pad=True) instead.

        Parameters
        ----------
        other : Vector

        Returns
        -------
        Vector

        Raises
        ------
        InvalidOperandError
            If other is not a Vector, or dimensions don't match.
        """
        return self.add(other, pad=False)

    def add(self, other: "Vector", pad: bool = False) -> "Vector":
        """
        Add two vectors component-wise, with optional zero-padding.

        Parameters
        ----------
        other : Vector
        pad : bool, optional
            If True, a shorter vector is treated as having 0 for
            its missing trailing components. Defaults to False.

        Returns
        -------
        Vector

        Raises
        ------
        InvalidOperandError
            If other is not a Vector, or dimensions don't match
            and pad is False.
        """
        a, b = self._padded_pair(other, "add", pad)
        return Vector(x + y for x, y in zip(a, b))

    def __sub__(self, other: "Vector") -> "Vector":
        """
        Subtract two vectors component-wise. Requires equal
        dimensions; for zero-padded subtraction, use
        subtract(other, pad=True) instead.

        Parameters
        ----------
        other : Vector

        Returns
        -------
        Vector

        Raises
        ------
        InvalidOperandError
            If other is not a Vector, or dimensions don't match.
        """
        return self.subtract(other, pad=False)

    def subtract(self, other: "Vector", pad: bool = False) -> "Vector":
        """
        Subtract two vectors component-wise, with optional
        zero-padding.

        Parameters
        ----------
        other : Vector
        pad : bool, optional
            If True, a shorter vector is treated as having 0 for
            its missing trailing components. Defaults to False.

        Returns
        -------
        Vector

        Raises
        ------
        InvalidOperandError
            If other is not a Vector, or dimensions don't match
            and pad is False.
        """
        a, b = self._padded_pair(other, "subtract", pad)
        return Vector(x - y for x, y in zip(a, b))

    def __mul__(self, scalar) -> "Vector":
        """
        Multiply this vector by a scalar.

        Parameters
        ----------
        scalar : int or float

        Returns
        -------
        Vector

        Raises
        ------
        InvalidOperandError
            If scalar is not an int/float (or is a bool).
        """
        if isinstance(scalar, bool) or not isinstance(scalar, (int, float)):
            raise InvalidOperandError("can only multiply Vector by a scalar (int or float)")
        return Vector(c * scalar for c in self._components)

    def __rmul__(self, scalar) -> "Vector":
        """
        Support scalar * vector (reversed operand order).

        Parameters
        ----------
        scalar : int or float

        Returns
        -------
        Vector
        """
        return self.__mul__(scalar)

    def dot(self, other: "Vector", pad: bool = False) -> float:
        """
        Compute the dot product with another vector.

        dot = sum(a_i * b_i for each component)

        Parameters
        ----------
        other : Vector
        pad : bool, optional
            If True, a shorter vector is treated as having 0 for
            its missing trailing components (which contribute 0 to
            the sum either way). Defaults to False.

        Returns
        -------
        float

        Raises
        ------
        InvalidOperandError
            If other is not a Vector, or dimensions don't match
            and pad is False.
        """
        a, b = self._padded_pair(other, "dot", pad)
        return sum(x * y for x, y in zip(a, b))

    def cross(self, other: "Vector") -> "Vector":
        """
        Compute the cross product with another vector.

        Cross product is only defined for 3-dimensional vectors —
        padding does not apply here, since cross product has no
        meaningful definition outside 3D (there is no sensible
        "missing component" interpretation to pad toward).

        Parameters
        ----------
        other : Vector

        Returns
        -------
        Vector
            A new 3D Vector perpendicular to both self and other.

        Raises
        ------
        InvalidOperandError
            If other is not a Vector.
        UndefinedOperationError
            If self or other is not exactly 3-dimensional.
        """
        if not isinstance(other, Vector):
            raise InvalidOperandError("can only cross Vector with Vector")
        if self.dimension != 3 or other.dimension != 3:
            raise UndefinedOperationError("cross product is only defined for 3D vectors")

        ax, ay, az = self._components
        bx, by, bz = other._components
        return Vector([
            ay * bz - az * by,
            az * bx - ax * bz,
            ax * by - ay * bx,
        ])

    def magnitude(self) -> float:
        """
        Return the magnitude (length) of this vector.

        Returns
        -------
        float
            sqrt(sum of squares of components)
        """
        return math.sqrt(sum(c ** 2 for c in self._components))

    def normalize(self) -> "Vector":
        """
        Return a unit vector (magnitude 1) in the same direction.

        Returns
        -------
        Vector

        Raises
        ------
        UndefinedOperationError
            If this is the zero vector (magnitude 0).
        """
        mag = self.magnitude()
        if mag == 0:
            raise UndefinedOperationError("cannot normalize the zero vector")
        return Vector(c / mag for c in self._components)

    def __neg__(self) -> "Vector":
        """
        Returns
        -------
        Vector
            A new Vector with every component sign-flipped.
        """
        return Vector(-c for c in self._components)
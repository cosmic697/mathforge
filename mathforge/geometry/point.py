"""
mathforge/geometry/point.py

Point

Represents a 2D point (x, y), with distance calculation to other points. Foundational object for the rest of the geometry module — Line, Triangle, and Circle are all built from Points.
"""

import math

from mathforge.core.errors import InvalidOperandError


class Point:
    """
    A 2D point with x and y coordinates.

    Point instances are immutable.

    Attributes
    ----------
    x : float
    y : float

    Examples
    --------
    >>> Point(0, 0).distance_to(Point(3, 4))
    5.0
    """

    def __init__(self, x: float, y: float):
        """
        Construct a Point.

        Parameters
        ----------
        x : float
        y : float

        Raises
        ------
        InvalidOperandError
            If x or y is not an int/float, or is a bool.
        """
        if isinstance(x, bool) or isinstance(y, bool):
            raise InvalidOperandError("x and y must be numbers, not booleans.")
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise InvalidOperandError("x and y must be int or float.")

        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        """float: The x-coordinate."""
        return self._x

    @property
    def y(self) -> float:
        """float: The y-coordinate."""
        return self._y

    def distance_to(self, other: "Point") -> float:
        """
        Return the Euclidean distance to another point.

        distance = sqrt((x2-x1)^2 + (y2-y1)^2)

        Parameters
        ----------
        other : Point

        Returns
        -------
        float

        Raises
        ------
        InvalidOperandError
            If other is not a Point.
        """
        if not isinstance(other, Point):
            raise InvalidOperandError("can only compute distance to another Point")
        return math.sqrt((other._x - self._x) ** 2 + (other._y - self._y) ** 2)

    def midpoint(self, other: "Point") -> "Point":
        """
        Return the midpoint between this point and another.

        Parameters
        ----------
        other : Point

        Returns
        -------
        Point

        Raises
        ------
        InvalidOperandError
            If other is not a Point.
        """
        if not isinstance(other, Point):
            raise InvalidOperandError("can only compute midpoint with another Point")
        return Point((self._x + other._x) / 2, (self._y + other._y) / 2)

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            In the form "Point(1.0, 2.0)".
        """
        return f"Point({self._x}, {self._y})"

    def __str__(self) -> str:
        """
        Returns
        -------
        str
            In the form "(1.0, 2.0)".
        """
        return f"({self._x}, {self._y})"

    def __eq__(self, other: object) -> bool:
        """
        Check equality: same x and y.

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            NotImplemented if other is not a Point.
        """
        if not isinstance(other, Point):
            return NotImplemented
        return self._x == other._x and self._y == other._y

    def __hash__(self) -> int:
        """
        Returns
        -------
        int
            Hash of (x, y). Coordinates are stored as exact floats from construction (no accumulated arithmetic drift like ComplexNumber/Decimal have), so ordinary equality/hash is safe here — unlike ComplexNumber, this isn't tolerance-based.
        """
        return hash((self._x, self._y))
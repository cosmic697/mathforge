"""
mathforge/geometry/triangle.py

Triangle

Represents a triangle defined by three Points, with perimeter,area, and a classification by side lengths.
"""

from mathforge.geometry.point import Point
from mathforge.core.errors import InvalidOperandError
from mathforge.core.constants import EPSILON


class Triangle:
    """
    A triangle defined by three points.

    Triangle instances are immutable.

    Attributes
    ----------
    a : Point
    b : Point
    c : Point

    Examples
    --------
    >>> Triangle(Point(0, 0), Point(4, 0), Point(0, 3)).area()
    6.0
    """

    def __init__(self, a: Point, b: Point, c: Point):
        """
        Construct a Triangle from three points.

        Parameters
        ----------
        a : Point
        b : Point
        c : Point

        Raises
        ------
        InvalidOperandError
            If a, b, or c is not a Point, any two points coincide,or all three points are collinear (zero-area — not areal triangle).
        """
        if not isinstance(a, Point) or not isinstance(b, Point) or not isinstance(c, Point):
            raise InvalidOperandError("a, b, and c must be Points.")
        if a == b or b == c or a == c:
            raise InvalidOperandError("the three points must be distinct.")

        self._a, self._b, self._c = a, b, c

        # Reject collinear points using the shoelace formula itself:
        # if the "signed area" comes out to 0, the three points lie
        # on one line and don't form a real triangle.
        if abs(self._signed_area_x2()) < EPSILON:
            raise InvalidOperandError("the three points are collinear; not a valid triangle.")

    def _signed_area_x2(self) -> float:
        """
        Internal helper: twice the signed area, via the shoelace formula. Used by both the linearity check in __init__ and area().
        """
        ax, ay = self._a.x, self._a.y
        bx, by = self._b.x, self._b.y
        cx, cy = self._c.x, self._c.y
        return ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)

    @property
    def a(self) -> Point:
        """Point: The first vertex."""
        return self._a

    @property
    def b(self) -> Point:
        """Point: The second vertex."""
        return self._b

    @property
    def c(self) -> Point:
        """Point: The third vertex."""
        return self._c

    def side_lengths(self) -> tuple:
        """
        Return the three side lengths.

        Returns
        -------
        tuple of float
            (|AB|, |BC|, |CA|) — the three sides, in that order.
        """
        return (
            self._a.distance_to(self._b),
            self._b.distance_to(self._c),
            self._c.distance_to(self._a),
        )

    def perimeter(self) -> float:
        """
        Return the perimeter (sum of the three side lengths).

        Returns
        -------
        float
        """
        return sum(self.side_lengths())

    def area(self) -> float:
        """
        Return the area, via the shoelace formula.

        Works directly from coordinates, without needing to fir identify a "base" and "height" the way the class (1/2 * base * height) formula does.

        Returns
        -------
        float
        """
        return abs(self._signed_area_x2()) / 2

    def triangle_type(self) -> str:
        """
        Classify the triangle by its side lengths.

        Returns
        -------
        str
            One of "equilateral" (all three sides equ "isosceles" (exactly two sides equal), or "scale (all three sides different). Side-length comparison use EPSILON tolerance, since side lengths are comp via sqrt and may carry tiny floating-point error.
        """
        s1, s2, s3 = self.side_lengths()
        eq_12 = abs(s1 - s2) < EPSILON
        eq_23 = abs(s2 - s3) < EPSILON
        eq_13 = abs(s1 - s3) < EPSILON

        if eq_12 and eq_23:
            return "equilateral"
        if eq_12 or eq_23 or eq_13:
            return "isosceles"
        return "scalene"

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            In the form "Triangle(Point(...), Point(...), Point(...))".
        """
        return f"Triangle({self._a!r}, {self._b!r}, {self._c!r})"

    def __eq__(self, other: object) -> bool:
        """
        Check equality: same three vertices, treat unordered set (Triangle(A,B,C) == Triangle(C,A,B) — Line, a triangle has no inherent direction/start po vertex order shouldn't matter for equality).

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            NotImplemented if other is not a Triangle.
        """
        if not isinstance(other, Triangle):
            return NotImplemented
        return {self._a, self._b, self._c} == {other._a, other._b, other._c}
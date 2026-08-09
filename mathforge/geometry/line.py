"""
mathforge/geometry/line.py

Line

Represents a 2D line segment defined by two Points, with length,midpoint, and slope.
"""

from mathforge.geometry.point import Point
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError


class Line:
    """
    A 2D line segment between two points.

    Line instances are immutable.

    Attributes
    ----------
    start : Point
    end : Point

    Examples
    --------
    >>> Line(Point(0, 0), Point(3, 4)).length()
    5.0
    """

    def __init__(self, start: Point, end: Point):
        """
        Construct a Line from two Points.

        Parameters
        ----------
        start : Point
        end : Point

        Raises
        ------
        InvalidOperandError
            If start or end is not a Point, or start == end (aline needs two distinct points — a single point has no length, midpoint, or slope).
        """
        if not isinstance(start, Point) or not isinstance(end, Point):
            raise InvalidOperandError("start and end must be Points.")
        if start == end:
            raise InvalidOperandError("start and end must be distinct points.")

        self._start = start
        self._end = end

    @property
    def start(self) -> Point:
        """Point: The starting point."""
        return self._start

    @property
    def end(self) -> Point:
        """Point: The ending point."""
        return self._end

    def length(self) -> float:
        """
        Return the length of the line segment.

        Returns
        -------
        float
        """
        return self._start.distance_to(self._end)

    def midpoint(self) -> Point:
        """
        Return the midpoint of the line segment.

        Returns
        -------
        Point
        """
        return self._start.midpoint(self._end)

    def slope(self) -> float:
        """
        Return the slope of the line.

        slope = (y2 - y1) / (x2 - x1)

        Returns
        -------
        float

        Raises
        ------
        UndefinedOperationError
            If the line is vertical (x1 == x2), since slope undefined (division by zero) in that case.
        """
        dx = self._end.x - self._start.x
        if dx == 0:
            raise UndefinedOperationError("slope is undefined for a vertical line")
        dy = self._end.y - self._start.y
        return dy / dx

    def is_vertical(self) -> bool:
        """
        Returns
        -------
        bool
            True if start and end have the same x-coordinate.
        """
        return self._start.x == self._end.x

    def is_horizontal(self) -> bool:
        """
        Returns
        -------
        bool
            True if start and end have the same y-coordinate.
        """
        return self._start.y == self._end.y

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            In the form "Line(Point(0.0, 0.0), Point(3.0, 4.0))".
        """
        return f"Line({self._start!r}, {self._end!r})"

    def __eq__(self, other: object) -> bool:
        """
        Check equality: same start and end points, in the order (Line(A, B) != Line(B, A) — direction matters since a Line is a segment, not just an undirected pair).

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            NotImplemented if other is not a Line.
        """
        if not isinstance(other, Line):
            return NotImplemented
        return self._start == other._start and self._end == other.end
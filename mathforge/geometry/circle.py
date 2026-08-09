"""
mathforge/geometry/circle.py

Circle

Represents a circle defined by a center Point and a radius, with area, circumference, and point-containment checks.
"""

import math

from mathforge.geometry.point import Point
from mathforge.core.errors import InvalidOperandError
from mathforge.core.constants import EPSILON


class Circle:
    """
    A circle defined by a center point and a radius.

    Circle instances are immutable.

    Attributes
    ----------
    center : Point
    radius : float

    Examples
    --------
    >>> Circle(Point(0, 0), 5).area()
    78.53981633974483
    """

    def __init__(self, center: Point, radius: float):
        """
        Construct a Circle.

        Parameters
        ----------
        center : Point
        radius : float
            Must be a positive number.

        Raises
        ------
        InvalidOperandError
            If center is not a Point, radius is not an int/float
            (or is a bool), or radius is not positive.
        """
        if not isinstance(center, Point):
            raise InvalidOperandError("center must be a Point.")
        if isinstance(radius, bool) or not isinstance(radius, (int, float)):
            raise InvalidOperandError("radius must be an int or float.")
        if radius <= 0:
            raise InvalidOperandError("radius must be positive.")

        self._center = center
        self._radius = float(radius)

    @property
    def center(self) -> Point:
        """Point: The center point."""
        return self._center

    @property
    def radius(self) -> float:
        """float: The radius."""
        return self._radius

    def area(self) -> float:
        """
        Return the area: pi * r^2.

        Returns
        -------
        float
        """
        return math.pi * self._radius ** 2

    def circumference(self) -> float:
        """
        Return the circumference: 2 * pi * r.

        Returns
        -------
        float
        """
        return 2 * math.pi * self._radius

    def contains_point(self, point: Point) -> bool:
        """
        Return whether a point lies inside the circle or exact on its boundary (distance from center <= radius, with EPSILON tolerance for the boundary case).

        Parameters
        ----------
        point : Point

        Returns
        -------
        bool

        Raises
        ------
        InvalidOperandError
            If point is not a Point.
        """
        if not isinstance(point, Point):
            raise InvalidOperandError("point must be a Point.")
        distance = self._center.distance_to(point)
        return distance <= self._radius + EPSILON

    def intersects(self, other: "Circle") -> bool:
        """
        Return whether this circle overlaps with another circle (their boundaries cross, or one is inside the other, or they're tangent).

        Two circles overlap unless the distance between centers is greater than the sum of their radii (too far apart) or less than the absolute difference of their radii (one is strictly nested inside the other with no contact).

        Parameters
        ----------
        other : Circle

        Returns
        -------
        bool

        Raises
        ------
        InvalidOperandError
            If other is not a Circle.
        """
        if not isinstance(other, Circle):
            raise InvalidOperandError("other must be a Circle.")
        distance = self._center.distance_to(other._center)
        radius_sum = self._radius + other._radius
        radius_diff = abs(self._radius - other._radius)
        return radius_diff - EPSILON <= distance <= radius_sum + EPSILON

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            In the form "Circle(Point(0.0, 0.0), 5.0)".
        """
        return f"Circle({self._center!r}, {self._radius})"

    def __eq__(self, other: object) -> bool:
        """
        Check equality: same center and same radius.

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            NotImplemented if other is not a Circle.
        """
        if not isinstance(other, Circle):
            return NotImplemented
        return self._center == other._center and abs(self._radius - other._radius) < EPSILON
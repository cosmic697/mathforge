"""
mathforge/geometry/tests/test_circle.py

Unit tests for the Circle class.
"""

import math
import pytest

from mathforge.geometry.circle import Circle
from mathforge.geometry.point import Point
from mathforge.core.errors import InvalidOperandError


# --- Construction ---

def test_construct_basic():
    c = Circle(Point(0, 0), 5)
    assert c.center == Point(0, 0)
    assert c.radius == 5.0


def test_construct_rejects_non_point_center():
    with pytest.raises(InvalidOperandError):
        Circle((0, 0), 5)


def test_construct_rejects_non_numeric_radius():
    with pytest.raises(InvalidOperandError):
        Circle(Point(0, 0), "5")


def test_construct_rejects_bool_radius():
    with pytest.raises(InvalidOperandError):
        Circle(Point(0, 0), True)


def test_construct_rejects_zero_radius():
    with pytest.raises(InvalidOperandError):
        Circle(Point(0, 0), 0)


def test_construct_rejects_negative_radius():
    with pytest.raises(InvalidOperandError):
        Circle(Point(0, 0), -5)


# --- area / circumference ---

def test_area():
    c = Circle(Point(0, 0), 5)
    assert abs(c.area() - (math.pi * 25)) < 1e-9


def test_circumference():
    c = Circle(Point(0, 0), 5)
    assert abs(c.circumference() - (2 * math.pi * 5)) < 1e-9


# --- contains_point ---

def test_contains_center():
    c = Circle(Point(0, 0), 5)
    assert c.contains_point(Point(0, 0)) is True


def test_contains_point_inside():
    c = Circle(Point(0, 0), 5)
    assert c.contains_point(Point(1, 1)) is True


def test_contains_point_on_boundary():
    c = Circle(Point(0, 0), 5)
    assert c.contains_point(Point(3, 4)) is True  # distance exactly 5


def test_contains_point_outside():
    c = Circle(Point(0, 0), 5)
    assert c.contains_point(Point(10, 10)) is False


def test_contains_point_rejects_non_point():
    c = Circle(Point(0, 0), 5)
    with pytest.raises(InvalidOperandError):
        c.contains_point((1, 1))


# --- intersects ---

def test_intersects_overlapping():
    a = Circle(Point(0, 0), 5)
    b = Circle(Point(3, 0), 5)
    assert a.intersects(b) is True


def test_intersects_too_far_apart():
    a = Circle(Point(0, 0), 1)
    b = Circle(Point(100, 0), 1)
    assert a.intersects(b) is False


def test_intersects_one_nested_inside_other():
    a = Circle(Point(0, 0), 10)
    b = Circle(Point(0, 0), 1)  # concentric, fully inside a, no boundary contact
    assert a.intersects(b) is False


def test_intersects_tangent_externally():
    a = Circle(Point(0, 0), 3)
    b = Circle(Point(6, 0), 3)  # distance == sum of radii, exactly touching
    assert a.intersects(b) is True


def test_intersects_rejects_non_circle():
    a = Circle(Point(0, 0), 5)
    with pytest.raises(InvalidOperandError):
        a.intersects((0, 0, 5))


# --- repr / eq ---

def test_repr():
    assert repr(Circle(Point(0, 0), 5)) == "Circle(Point(0.0, 0.0), 5.0)"


def test_eq_true():
    assert Circle(Point(0, 0), 5) == Circle(Point(0, 0), 5)


def test_eq_false_different_radius():
    assert Circle(Point(0, 0), 5) != Circle(Point(0, 0), 6)


def test_eq_false_different_center():
    assert Circle(Point(0, 0), 5) != Circle(Point(1, 0), 5)


def test_eq_non_circle_returns_false():
    assert (Circle(Point(0, 0), 5) == "not a circle") is False
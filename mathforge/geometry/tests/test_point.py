"""
mathforge/geometry/tests/test_point.py

Unit tests for the Point class.
"""

import pytest

from mathforge.geometry.point import Point
from mathforge.core.errors import InvalidOperandError


# --- Construction ---

def test_construct_basic():
    p = Point(3, 4)
    assert p.x == 3.0
    assert p.y == 4.0


def test_construct_converts_to_float():
    p = Point(3, 4)
    assert isinstance(p.x, float)
    assert isinstance(p.y, float)


def test_construct_negative_coordinates():
    p = Point(-1, -2)
    assert p.x == -1.0
    assert p.y == -2.0


def test_construct_rejects_bool():
    with pytest.raises(InvalidOperandError):
        Point(True, 2)


def test_construct_rejects_non_numeric():
    with pytest.raises(InvalidOperandError):
        Point("3", 4)


# --- distance_to ---

def test_distance_classic_3_4_5_triangle():
    assert Point(0, 0).distance_to(Point(3, 4)) == 5.0


def test_distance_to_self_is_zero():
    p = Point(5, 5)
    assert p.distance_to(p) == 0.0


def test_distance_is_symmetric():
    a, b = Point(1, 2), Point(4, 6)
    assert a.distance_to(b) == b.distance_to(a)


def test_distance_rejects_non_point():
    with pytest.raises(InvalidOperandError):
        Point(0, 0).distance_to((3, 4))


# --- midpoint ---

def test_midpoint():
    a, b = Point(0, 0), Point(4, 6)
    assert a.midpoint(b) == Point(2, 3)


def test_midpoint_is_symmetric():
    a, b = Point(1, 1), Point(5, 5)
    assert a.midpoint(b) == b.midpoint(a)


def test_midpoint_rejects_non_point():
    with pytest.raises(InvalidOperandError):
        Point(0, 0).midpoint(5)


# --- String representation ---

def test_repr():
    assert repr(Point(1, 2)) == "Point(1.0, 2.0)"


def test_str():
    assert str(Point(1, 2)) == "(1.0, 2.0)"


# --- Equality / hashing ---

def test_eq_true():
    assert Point(1, 2) == Point(1, 2)


def test_eq_false():
    assert Point(1, 2) != Point(1, 3)


def test_eq_non_point_returns_false():
    assert (Point(1, 2) == (1, 2)) is False


def test_hashable_in_set():
    s = {Point(1, 2), Point(1, 2), Point(3, 4)}
    assert len(s) == 2
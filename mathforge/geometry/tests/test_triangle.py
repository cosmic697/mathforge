"""
mathforge/geometry/tests/test_triangle.py

Unit tests for the Triangle class.
"""

import pytest

from mathforge.geometry.triangle import Triangle
from mathforge.geometry.point import Point
from mathforge.core.errors import InvalidOperandError


# --- Construction ---

def test_construct_basic():
    t = Triangle(Point(0, 0), Point(4, 0), Point(0, 3))
    assert t.a == Point(0, 0)


def test_construct_rejects_non_point():
    with pytest.raises(InvalidOperandError):
        Triangle((0, 0), Point(1, 0), Point(0, 1))


def test_construct_rejects_duplicate_point():
    with pytest.raises(InvalidOperandError):
        Triangle(Point(0, 0), Point(0, 0), Point(1, 1))


def test_construct_rejects_collinear_points():
    with pytest.raises(InvalidOperandError):
        Triangle(Point(0, 0), Point(1, 1), Point(2, 2))


def test_construct_rejects_collinear_horizontal():
    with pytest.raises(InvalidOperandError):
        Triangle(Point(0, 5), Point(1, 5), Point(2, 5))


# --- side_lengths / perimeter ---

def test_side_lengths_3_4_5():
    t = Triangle(Point(0, 0), Point(4, 0), Point(0, 3))
    sides = t.side_lengths()
    assert abs(sorted(sides)[0] - 3.0) < 1e-9
    assert abs(sorted(sides)[1] - 4.0) < 1e-9
    assert abs(sorted(sides)[2] - 5.0) < 1e-9


def test_perimeter_3_4_5():
    t = Triangle(Point(0, 0), Point(4, 0), Point(0, 3))
    assert abs(t.perimeter() - 12.0) < 1e-9


# --- area ---

def test_area_right_triangle():
    # legs 4 and 3 -> area = 0.5 * 4 * 3 = 6
    t = Triangle(Point(0, 0), Point(4, 0), Point(0, 3))
    assert abs(t.area() - 6.0) < 1e-9


def test_area_independent_of_vertex_order():
    # shoelace formula's abs() should make winding order not matter
    t1 = Triangle(Point(0, 0), Point(4, 0), Point(0, 3))
    t2 = Triangle(Point(0, 0), Point(0, 3), Point(4, 0))
    assert abs(t1.area() - t2.area()) < 1e-9


# --- triangle_type ---

def test_type_equilateral():
    import math
    # equilateral triangle, side length 2
    t = Triangle(Point(0, 0), Point(2, 0), Point(1, math.sqrt(3)))
    assert t.triangle_type() == "equilateral"


def test_type_isosceles():
    t = Triangle(Point(0, 0), Point(4, 0), Point(2, 3))
    assert t.triangle_type() == "isosceles"


def test_type_scalene():
    t = Triangle(Point(0, 0), Point(4, 0), Point(1, 2))
    assert t.triangle_type() == "scalene"


# --- repr / eq ---

def test_repr():
    t = Triangle(Point(0, 0), Point(1, 0), Point(0, 1))
    assert "Triangle(" in repr(t)


def test_eq_true_same_order():
    t1 = Triangle(Point(0, 0), Point(1, 0), Point(0, 1))
    t2 = Triangle(Point(0, 0), Point(1, 0), Point(0, 1))
    assert t1 == t2


def test_eq_true_different_order():
    t1 = Triangle(Point(0, 0), Point(1, 0), Point(0, 1))
    t2 = Triangle(Point(0, 1), Point(0, 0), Point(1, 0))
    assert t1 == t2


def test_eq_false_different_vertices():
    t1 = Triangle(Point(0, 0), Point(1, 0), Point(0, 1))
    t2 = Triangle(Point(0, 0), Point(2, 0), Point(0, 1))
    assert t1 != t2


def test_eq_non_triangle_returns_false():
    t = Triangle(Point(0, 0), Point(1, 0), Point(0, 1))
    assert (t == "not a triangle") is False
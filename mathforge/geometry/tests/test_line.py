"""
mathforge/geometry/tests/test_line.py

Unit tests for the Line class.
"""

import pytest

from mathforge.geometry.line import Line
from mathforge.geometry.point import Point
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError


# --- Construction ---

def test_construct_basic():
    line = Line(Point(0, 0), Point(3, 4))
    assert line.start == Point(0, 0)
    assert line.end == Point(3, 4)


def test_construct_rejects_non_point_start():
    with pytest.raises(InvalidOperandError):
        Line((0, 0), Point(1, 1))


def test_construct_rejects_non_point_end():
    with pytest.raises(InvalidOperandError):
        Line(Point(0, 0), (1, 1))


def test_construct_rejects_identical_points():
    with pytest.raises(InvalidOperandError):
        Line(Point(1, 1), Point(1, 1))


# --- length ---

def test_length_classic_3_4_5():
    assert Line(Point(0, 0), Point(3, 4)).length() == 5.0


def test_length_horizontal():
    assert Line(Point(0, 0), Point(5, 0)).length() == 5.0


# --- midpoint ---

def test_midpoint():
    line = Line(Point(0, 0), Point(4, 6))
    assert line.midpoint() == Point(2, 3)


# --- slope ---

def test_slope_positive():
    assert Line(Point(0, 0), Point(2, 4)).slope() == 2.0


def test_slope_negative():
    assert Line(Point(0, 4), Point(2, 0)).slope() == -2.0


def test_slope_zero_for_horizontal():
    assert Line(Point(0, 3), Point(5, 3)).slope() == 0.0


def test_slope_vertical_raises():
    with pytest.raises(UndefinedOperationError):
        Line(Point(2, 0), Point(2, 5)).slope()


# --- is_vertical / is_horizontal ---

def test_is_vertical_true():
    assert Line(Point(2, 0), Point(2, 5)).is_vertical() is True


def test_is_vertical_false():
    assert Line(Point(0, 0), Point(2, 5)).is_vertical() is False


def test_is_horizontal_true():
    assert Line(Point(0, 3), Point(5, 3)).is_horizontal() is True


def test_is_horizontal_false():
    assert Line(Point(0, 0), Point(5, 3)).is_horizontal() is False


# --- repr / eq ---

def test_repr():
    assert repr(Line(Point(0, 0), Point(3, 4))) == "Line(Point(0.0, 0.0), Point(3.0, 4.0))"


def test_eq_true():
    assert Line(Point(0, 0), Point(1, 1)) == Line(Point(0, 0), Point(1, 1))


def test_eq_false_reversed_direction():
    # deliberately NOT equal — direction matters (see docstring)
    assert Line(Point(0, 0), Point(1, 1)) != Line(Point(1, 1), Point(0, 0))


def test_eq_non_line_returns_false():
    assert (Line(Point(0, 0), Point(1, 1)) == "not a line") is False
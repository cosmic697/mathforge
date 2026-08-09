"""
mathforge/numerical_methods/tests/test_root_finding.py

Unit tests for bisection and newton_raphson.
"""

import pytest

from mathforge.numerical_methods.root_finding import bisection, newton_raphson , secant
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError, ConvergenceError


# --- bisection ---

def test_bisection_finds_sqrt_2():
    # f(x) = x^2 - 2, root is sqrt(2) ~= 1.41421356
    root = bisection(lambda x: x ** 2 - 2, 0, 2)
    assert abs(root - 1.4142135623730951) < 1e-6


def test_bisection_finds_negative_root():
    # f(x) = x^2 - 4, roots at -2 and 2; search [-3, -1] finds -2
    root = bisection(lambda x: x ** 2 - 4, -3, -1)
    assert abs(root - (-2.0)) < 1e-6


def test_bisection_exact_root_at_endpoint():
    root = bisection(lambda x: x - 2, 0, 4)
    assert abs(root - 2.0) < 1e-6


def test_bisection_rejects_a_greater_equal_b():
    with pytest.raises(InvalidOperandError):
        bisection(lambda x: x, 5, 1)


def test_bisection_rejects_same_sign_endpoints():
    # f(x) = x^2 + 1 has no real root; f(0)=1, f(2)=5, both positive
    with pytest.raises(UndefinedOperationError):
        bisection(lambda x: x ** 2 + 1, 0, 2)


def test_bisection_rejects_non_numeric_bounds():
    with pytest.raises(InvalidOperandError):
        bisection(lambda x: x, "0", 2)


# --- newton_raphson ---

def test_newton_raphson_finds_sqrt_2():
    root = newton_raphson(
        f=lambda x: x ** 2 - 2,
        f_prime=lambda x: 2 * x,
        x0=1.0,
    )
    assert abs(root - 1.4142135623730951) < 1e-9


def test_newton_raphson_finds_cube_root():
    # f(x) = x^3 - 27, root at x=3
    root = newton_raphson(
        f=lambda x: x ** 3 - 27,
        f_prime=lambda x: 3 * x ** 2,
        x0=1.0,
    )
    assert abs(root - 3.0) < 1e-9


def test_newton_raphson_rejects_non_numeric_x0():
    with pytest.raises(InvalidOperandError):
        newton_raphson(lambda x: x, lambda x: 1, "1")


def test_newton_raphson_zero_derivative_raises():
    # f(x) = x^2 + 1 has derivative 2x, which is 0 exactly at x0=0
    with pytest.raises(UndefinedOperationError):
        newton_raphson(
            f=lambda x: x ** 2 + 1,
            f_prime=lambda x: 2 * x,
            x0=0.0,
        )


def test_newton_raphson_convergence_error_on_bad_setup():
    # f with derivative that keeps bouncing the guess around,
    # never actually converging within max_iterations
    with pytest.raises(ConvergenceError):
        newton_raphson(
            f=lambda x: x ** 3 - 2 * x + 2,
            f_prime=lambda x: 3 * x ** 2 - 2,
            x0=0.0,
            max_iterations=5,
        )
# --- secant ---

def test_secant_finds_sqrt_2():
    root = secant(lambda x: x ** 2 - 2, x0=0.0, x1=2.0)
    assert abs(root - 1.4142135623730951) < 1e-9


def test_secant_finds_cube_root():
    root = secant(lambda x: x ** 3 - 27, x0=1.0, x1=4.0)
    assert abs(root - 3.0) < 1e-9


def test_secant_rejects_equal_starting_points():
    with pytest.raises(InvalidOperandError):
        secant(lambda x: x, x0=1.0, x1=1.0)


def test_secant_rejects_non_numeric_x0():
    with pytest.raises(InvalidOperandError):
        secant(lambda x: x, x0="0", x1=2.0)


def test_secant_zero_denominator_raises():
    # f is constant on the two starting points -> f1 - f0 == 0 immediately
    with pytest.raises(UndefinedOperationError):
        secant(lambda x: 5.0, x0=0.0, x1=1.0)
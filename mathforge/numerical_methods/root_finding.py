"""
mathforge/numerical_methods/root_finding.py

Root-finding algorithms: bisection, Newton-Raphson.

Each function takes a mathematical function f as its first argument (a Python callable, f: float -> float) and searches for an x where f(x) == 0 (a "root" of f).
"""

from mathforge.core.errors import InvalidOperandError, UndefinedOperationError, ConvergenceError
from mathforge.core.constants import EPSILON

def bisection(f, a: float, b: float, tolerance: float = EPSILON, max_iterations: int = 200) -> float:
    """
    Find a root of f within [a, b] using the bisection method.

    Repeatedly halves the interval [a, b], keeping whichever half still contains a sign change (and therefore still contains a root, by the Intermediate Value Theorem) — the interval shrinks geometrically until it's narrower than `tolerance`.

    Requires f(a) and f(b) to have opposite signs — this guarantees (by the Intermediate Value Theorem) that a root exists somewhere between them, since a continuous function can't go from negative to positive without crossing zero.

    Parameters
    ----------
    f : callable
        A function taking a float and returning a float.
    a : float
        Left endpoint of the search interval.
    b : float
        Right endpoint of the search interval.
    tolerance : float, optional
        Stop once the interval is narrower than this. Defaults to EPSILON.
    max_iterations : int, optional
        Safety limit in case something prevents convergence. Defaults to 200.

    Returns
    -------
    float
        An x with f(x) approximately 0.

    Raises
    ------
    InvalidOperandError
        If a, b, tolerance are not numbers, or a >= b.
    UndefinedOperationError
        If f(a) and f(b) do not have opposite signs (bisection cannot guarantee a root exists in this case).
    ConvergenceError
        If max_iterations is reached without converging within tolerance (should not normally happen given the geometric shrink rate, but guards against a pathological f).
    """
    if isinstance(a, bool) or isinstance(b, bool) or not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise InvalidOperandError("a and b must be numbers.")
    if a >= b:
        raise InvalidOperandError("a must be less than b.")

    fa, fb = f(a), f(b)
    if fa == 0:
        return float(a)
    if fb == 0:
        return float(b)
    if (fa > 0) == (fb > 0):
        raise UndefinedOperationError(
            "f(a) and f(b) must have opposite signs for bisection to guarantee a root"
        )

    for _ in range(max_iterations):
        midpoint = (a + b) / 2
        f_mid = f(midpoint)

        if abs(f_mid) < tolerance or (b - a) / 2 < tolerance:
            return midpoint

        if (f_mid > 0) == (fa > 0):
            a, fa = midpoint, f_mid
        else:
            b, fb = midpoint, f_mid

    raise ConvergenceError(f"bisection did not converge within {max_iterations} iterations")


def newton_raphson(f, f_prime, x0: float, tolerance: float = EPSILON, max_iterations: int = 100) -> float:
    """
    Find a root of f near x0 using the Newton-Raphson method.

    Repeatedly follows the tangent line at the current guess down to where it crosses zero, using that as the next guess:

        x_next = x - f(x) / f'(x)
    Converges much faster than bisection when it converges at all, but has no guarantee of converging — a poor starting guess, a flat derivative near the root, or an oscillating f can all cause it to fail. Unlike bisection, it needs the DERIVATIVE of f, not just f itself.

    Parameters
    ----------
    f : callable
        A function taking a float and returning a float.
    f_prime : callable
        The derivative of f, same signature.
    x0 : float
        Starting guess.
    tolerance : float, optional
        Stop once |f(x)| is below this. Defaults to EPSILON.
    max_iterations : int, optional
        Defaults to 100.

    Returns
    -------
    float

    Raises
    ------
    InvalidOperandError
        If x0 is not a number.
    UndefinedOperationError
        If f_prime(x) is ever 0 during iteration (the tangent line is horizontal — no well-defined next guess).
    ConvergenceError
        If max_iterations is reached without converging.
    """
    if isinstance(x0, bool) or not isinstance(x0, (int, float)):
        raise InvalidOperandError("x0 must be a number.")

    x = float(x0)
    for _ in range(max_iterations):
        fx = f(x)
        if abs(fx) < tolerance:
            return x

        fpx = f_prime(x)
        if fpx == 0:
            raise UndefinedOperationError(
                f"derivative is zero at x={x}; Newton-Raphson cannot continue"
            )

        x = x - fx / fpx

    raise ConvergenceError(f"Newton-Raphson did not converge within {max_iterations} iterations")

def secant(f, x0: float, x1: float, tolerance: float = EPSILON, max_iterations: int = 100) -> float:
    """
    Find a root of f using the secant method, starting from two initial guesses x0 and x1.

    Like Newton-Raphson, but approximates the derivative using the slope between the two most recent guesses instead of requiring an actual derivative function:

        x_next = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))

    Converges more slowly than Newton-Raphson in general, but does
    not need f' supplied.

    Parameters
    ----------
    f : callable
        A function taking a float and returning a float.
    x0 : float
        First starting guess.
    x1 : float
        Second starting guess. Must differ from x0.
    tolerance : float, optional
        Stop once |f(x1)| is below this. Defaults to EPSILON.
    max_iterations : int, optional
        Defaults to 100.

    Returns
    -------
    float

    Raises
    ------
    InvalidOperandError
        If x0 or x1 is not a number, or x0 == x1 (the initial secant line would be undefined — division by zero on the very first step).
    UndefinedOperationError
        If f(x1) - f(x0) is ever 0 during iteration (the secant line is horizontal — no well-defined next guess).
    ConvergenceError
        If max_iterations is reached without converging.
    """
    if isinstance(x0, bool) or isinstance(x1, bool) or not isinstance(x0, (int, float)) or not isinstance(x1, (int, float)):
        raise InvalidOperandError("x0 and x1 must be numbers.")
    if x0 == x1:
        raise InvalidOperandError("x0 and x1 must be different starting points.")

    x0, x1 = float(x0), float(x1)
    f0, f1 = f(x0), f(x1)

    for _ in range(max_iterations):
        if abs(f1) < tolerance:
            return x1

        denominator = f1 - f0
        if denominator == 0:
            raise UndefinedOperationError(
                f"f(x1) - f(x0) is zero at x0={x0}, x1={x1}; secant method cannot continue"
            )

        x_next = x1 - f1 * (x1 - x0) / denominator

        x0, f0 = x1, f1
        x1 = x_next
        f1 = f(x1)

    raise ConvergenceError(f"secant method did not converge within {max_iterations} iterations")
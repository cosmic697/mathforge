"""
mathforge/arithmetic/tests/test_gcd.py

Unit tests for the Greatest Common Divisor (GCD) algorithm.
"""

import pytest
from mathforge.arithmetic.algorithms.gcd import gcd
from mathforge.core.errors import InvalidOperandError,UndefinedOperationError

def test_gcd_normal_cases():
    assert gcd(12, 18) == 6
    assert gcd(48, 18) == 6
    assert gcd(100, 25) == 25
    assert gcd(7, 13) == 1


def test_gcd_equal_numbers():
    assert gcd(5, 5) == 5
    assert gcd(1000, 1000) == 1000


def test_gcd_zero_cases():
    assert gcd(0, 10) == 10
    assert gcd(10, 0) == 10


def test_gcd_negative_numbers():
    assert gcd(-12, 18) == 6
    assert gcd(12, -18) == 6
    assert gcd(-12, -18) == 6

@pytest.mark.parametrize("a, b", [
    (12.5, 5),
    ("12", 5),
    (True, 5),
    ([], 5),
    (None, 5),
])
def test_gcd_rejects_invalid_types(a, b):
    with pytest.raises(InvalidOperandError):
        gcd(a, b)


def test_gcd_zero_zero_is_undefined():
    with pytest.raises(UndefinedOperationError):
        gcd(0, 0)
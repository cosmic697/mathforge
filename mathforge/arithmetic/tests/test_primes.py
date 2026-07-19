"""
mathforge/arithmetic/tests/test_primes.py

Unit test for the primes algorithm
"""
import pytest
from mathforge.arithmetic.algorithms.primes import is_prime
from mathforge.core.errors import InvalidOperandError


def test_primes_cases():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(5) is True
    assert is_prime(7) is True
    assert is_prime(11) is True
    assert is_prime(13) is True
    assert is_prime(97) is True


def test_composite_cases():
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(9) is False
    assert is_prime(10) is False
    assert is_prime(100) is False


def test_edge_cases():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(-1) is False
    assert is_prime(-17) is False


@pytest.mark.parametrize( "a", [
        12.5,
        "12",
        True,
        [],
        None,
])
def test_primes_invalid_types(a):
    with pytest.raises(InvalidOperandError):
        is_prime(a)

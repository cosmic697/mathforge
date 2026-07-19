"""
mathforge/arithmetic/tests/test_lcm.py

Unit tests for the least common multiple(LCM) algorithm.
"""

import pytest
from mathforge.arithmetic.algorithms.lcm import lcm
from mathforge.core.errors import UndefinedOperationError, InvalidOperandError

def test_lcm_normal_cases():
    assert lcm(4, 6) == 12
    assert lcm(21, 6) == 42


def test_lcm_zero_and_nonzero():
    assert lcm(0, 5) == 0
    assert lcm(5, 0) == 0


def test_lcm_zero_zero_is_undefined():
    with pytest.raises(UndefinedOperationError):
        lcm(0, 0)


@pytest.mark.parametrize("a, b", [(True, 5), ("6", 4), (None, 4)])
def test_lcm_rejects_invalid_types(a, b):
    with pytest.raises(InvalidOperandError):
        lcm(a, b)
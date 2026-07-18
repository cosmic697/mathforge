"""
Unit tests for the primes algo
"""

from mathforge.arithmetic.algorithms.primes import is_prime

def run_tests()->None:
    """Run all prime test case"""

    print("Running prime test case")

    #prime number

    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(5) is True
    assert is_prime(7) is True
    assert is_prime(11) is True
    assert is_prime(13) is True
    assert is_prime(97) is True

    print("✓ Prime cases passed")

    #composite number 

    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(9) is False
    assert is_prime(10) is False
    assert is_prime(100) is False

    print("✓ Composite cases passed")

    #Edge cases

    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(-1) is False
    assert is_prime(-17) is False

    print("✓ Edge cases passed")

    # Invalid Types
    invalid_inputs = [
        12.5,
        "12",
        True,
        [],
        None,
    ]

    for a in invalid_inputs:
        try:
            is_prime(a)
        except TypeError:
            pass
        else:
            raise AssertionError(f"Expected TypeError for is_prime({a})")

    print("✓ Invalid type cases passed")

    print("\nAll prime tests passed successfully! 🎉")

if __name__ == "__main__":
    run_tests()
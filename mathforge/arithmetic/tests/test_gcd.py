"""
Unit tests for the Greatest Common Divisor (GCD) algorithm.
"""

from mathforge.arithmetic.algorithms.gcd import gcd


def run_tests() -> None:
    """Run all GCD test cases."""

    print("Running GCD Tests...\n")

    # Normal Cases

    assert gcd(12, 18) == 6
    assert gcd(48, 18) == 6
    assert gcd(100, 25) == 25
    assert gcd(7, 13) == 1

    print("✓ Normal cases passed")

    # Equal Numbers

    assert gcd(5, 5) == 5
    assert gcd(1000, 1000) == 1000

    print("✓ Equal number cases passed")

    # Zero Cases

    assert gcd(0, 10) == 10
    assert gcd(10, 0) == 10

    print("✓ Zero cases passed")

    # Negative Numbers

    assert gcd(-12, 18) == 6
    assert gcd(12, -18) == 6
    assert gcd(-12, -18) == 6

    print("✓ Negative number cases passed")

    # Invalid Types
    invalid_inputs = [
        (12.5, 5),
        ("12", 5),
        (True, 5),
        ([], 5),
        (None, 5),
    ]

    for a, b in invalid_inputs:
        try:
            gcd(a, b)
        except TypeError:
            pass
        else:
            raise AssertionError(f"Expected TypeError for gcd({a}, {b})")

    print("✓ Invalid type cases passed")

    # Undefined Case

    try:
        gcd(0, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for gcd(0, 0)")

    print("✓ Undefined case passed")

    print("\nAll GCD tests passed successfully! 🎉")

if __name__ == "__main__":
    run_tests()
"""
Unit tests for the LCM algo
"""

from mathforge.arithmetic.algorithms.lcm import lcm

def run_tests()->None:
    """Run all LCM test case"""

    print("Running LCM test case")

    #Normal case 

    assert lcm(4, 6) == 12
    assert lcm(6, 8) == 24
    assert lcm(7, 13) == 91
    assert lcm(5, 5) == 5

    print("✓ Normal cases passed")

    #Zero case

    assert lcm(0, 5) == 0
    assert lcm(5, 0) == 0

    print("✓ Zero cases passed")

    #Negative number 

    assert lcm(-4, 6) == 12
    assert lcm(4, -6) == 12
    assert lcm(-4, -6) == 12

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
            lcm(a, b)
        except TypeError:
            pass
        else:
            raise AssertionError(f"Expected TypeError for lcm({a}, {b})")

    print("✓ Invalid type cases passed")

    # Undefined Case

    try:
        lcm(0, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for gcd(0, 0)")

    print("✓ Undefined case passed")

    print("\nAll LCM tests passed successfully! 🎉")

if __name__ == "__main__":
    run_tests()
"""
PRIMES

this module provides the algorithm related to prime numbers.
"""
import math
from mathforge.core.errors import InvalidOperandError

def is_prime(n: int) ->int:
    """
    Determine if the number is prime or not.

    A prime is a positive integer greater than 1 and that has exactly two positive divisors: 1 and itself.

    Parameters
    ----------
    a : int
        integer to test for prime.

    Returns
    -------
    bool 
        True if the integer is prime, otherwise False.

    Raises
    ------
    TypeError
        If either not an integer.

    """

    #reject if boolean 
    if isinstance(n,bool):
        raise InvalidOperandError("Argument must be an integer, not a boolean")

    #validate type
    if not isinstance(n,int):
        raise InvalidOperandError("Argument must be an integer")
    
    #prime number must be greater than one
    if n<=1:
        return False
    
    #2 is the only even prime number 
    if n==2:
        return True
    
    #eliminate all other even numbers
    if n%2==0:
        return False
    
    #check odd divisor upto sqrt (n)
    limit=math.isqrt(n)

    divisor=3
    while divisor <=limit:
        if n%divisor ==0:
            return False
        divisor +=2

    return True

"""
LEAST COMMON MULTIPLE

this module provids an implementation of the Least Common Multiple(LCD) algorithm using the GCD algo
"""
from mathforge.arithmetic.algorithms.gcd import gcd
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError

def lcm(a: int, b: int)->int:
    """
    Compute the Least Common Multiple (LCM) of two integers.

    The LCM is the smallest positive integer that is divisible
    by both input integers.

    Parameters
    ----------
    a : int
        First integer.

    b : int
        Second integer.

    Returns
    -------
    int
        The least common multiple of the two integers.

    Raises
    ------
    TypeError
        If either argument is not an integer.

    ValueError
        If both arguments are zero.
    """

    # Reject booleans (bool is a subclass of int in Python)
    if isinstance(a,bool) or isinstance(b,bool):
        raise InvalidOperandError("Arguments must be integers, not booleans.")
    
    #validate type 
    if not isinstance(a,int) or not isinstance(b,int):
        raise InvalidOperandError("Argument must be a integer")
    #lcm(0,0) is undefined 
    if a==0 and b==0:
        raise UndefinedOperationError("LCM is undefined for (0,0)")
    
    #by defination LCM(0,n)=0
    if a==0 or b==0:
        return 0
    
    return abs( (a//gcd(a,b))*b)
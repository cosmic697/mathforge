"""
GREATEST COMMON DIVISOR(GCD)

this module provides an implementation of the euclidean algorithm for computing the Greatest Common Divisor(GCD) of two integers.
"""
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError

def gcd(a:int , b:int)->int:
    """
    compute the greatest common divisor (GCD) of two integers
    
    the GCD is the largest positive integer that divides both numbers without leaving a remainder.
    
    parameters
    ----------
    a : int 
        First integer
        
    b : int 
        Second integer 
    
    Returns
    -------
    int 
        the greatest common divisor of the two integers.
        
    Raises
    ------
    TypeError
        if either argument is not an integer.
        
    ValueError
        if both arguments are zero
    """

    #reject boolean 
    if isinstance(a,bool) or isinstance(b,bool):
        raise InvalidOperandError("argument must be integer , not boolean.")
    
    #validate type
    if not isinstance(a,int) or not isinstance(b,int):
        raise InvalidOperandError("arguments must be integers.")
    
    #GCD(0,0) is undefined
    if a==0 and b==0:
        raise UndefinedOperationError("GCD is undefined for (0,0)")

    #work with positive values 
    a=abs(a)
    b=abs(b)

    while b!=0:
        a,b=b,a%b

    return a

        
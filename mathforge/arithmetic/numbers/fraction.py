"""
mathforge/arithmetic/numbers/fraction.py

Fraction

Represents an exact rational number as numerator/denominator,
always kept in simplified form.
"""

from mathforge.core.constants import EPSILON
from mathforge.arithmetic.algorithms.gcd import gcd
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError
from mathforge.core.constants import EPSILON

class Fraction():
    """
    An exact rational number, represent as numerator/denominator.

    Fractions are always stored in simplified(lowest-terms) form , with the sign normalized onto the numerator (denominator is always positive). Fraction instances are immutable - every arithmetic operation return a new Fraction rather than modifying self.

    Attributes
    ----------
    numerator : int
        The simplified numerator (read-only).
    denominator : int
        The simplified denominator (read-only, always positive).

    
    """ 

    def __init__(self , numerator:int , denominator:int = 1):
        """
        construct a fraction and reduce it to its lowest terms
        
        Parameters:
        -----------
        numerator : int 
            the numerator
        denominator : int, optional
            The denominator. Must be non-zero. Defaults to 1, so Fraction(5) represents the whole number 5 as 5/1.

        Raises:
        ------

        InvalidOperandError
            if numerator or denominator is not an int or is an boolean.

        UndefinedOperationError
            if denominator is zero

        Notes:
        ------

        - if denominator is negative, the sign should be moved onto the numerator, so denominator is always stored positive.
        -use gcd() to reduce numerator/denominator ro lowest terms.
        -store result in self._numerator/ self._denominator     
        """

        # Reject booleans (bool is a subclass of int in Python)
        if isinstance(numerator,bool) or isinstance(denominator, bool):
            raise InvalidOperandError("arguments should be integer not boolean")
        
        #validate type 
        if not isinstance(numerator , int) or not isinstance(denominator , int):
            raise InvalidOperandError("argument should be a integers.")
        
        #denominator should not be zero 
        if denominator==0:
            raise UndefinedOperationError("denominator cannot be zero.")

        if denominator < 0:
            numerator , denominator = -numerator , -denominator

        common = gcd(numerator , denominator) if numerator!=0 else denominator
        self._numerator = numerator//common
        self._denominator= denominator//common

    @property
    def numerator(self)->int:
        """
        return a simplified numerator
        """
        return self._numerator

    @property
    def denominator(self)->int:
        """
        return a simplified denominator.
        """
        return self._denominator

    def __repr__(self)->int:
        """
        return the unambiguous developer representation.
        
        Returns
        -------
        str
            in the form 'Fraction(numerator,denominator)'
        """
        return f"Fraction({self._numerator}, {self._denominator})"

    def __str__(self)->str:
        """
        Return the human-readable string form.
        
        Returns
        -------
        str
            in the form "numerator/denominator."
        """
        return f"{self._numerator}/{self._denominator}"


    def __add__(self,other:"Fraction")->"Fraction":
        """
        Add two fractions.

        a/b + c/d = (a*d + c*b)/(b*d)
        
        Parameters
        ----------

        other:fraction
            the fraction to add.

        Return
        ------

        Fraction
            a new, simplified representing the sum.

        Raises
        ------

        InvalidOperandError
            id other is not fraction.  
        """

        if not isinstance(other,Fraction):
            raise InvalidOperandError("can only add fraction to fraction")
        return Fraction(
            self._numerator * other._denominator + other._numerator * self._denominator,self._denominator * other._denominator
        )

    def __sub__(self,other:"Fraction")->"Fraction":
        """
        
        Subtract another fraction from this one.
        
        a/b - c/d =(a*d -c*b)/(b*d)
        
        Parameters
        ----------
        
        other : Fraction
            The fraction to subtract.

        Return
        ------

        Fraction
        A new simplified Fraction representing  the difference.

        Raises
        ------
        InvalidOperandError
            if other is not a fraction.
        """
        if not isinstance(other,Fraction):
            raise InvalidOperandError("can only add fraction to fraction")
        return Fraction(
            self._numerator * other._denominator - other._numerator * self._denominator,self._denominator * other._denominator
        )

    def __mul__(self,other:"Fraction")->"Fraction":
        """
        Multiply two fractions.
        
        (a/b)*(c/d)=(a*c)/(b*d)
        
        Parameters
        ----------
        
        other : Fraction
            the fraction to multiply by.
            
        Returns
        -------
        
        Fraction
            A new , simplified Fraction representing the product.
            
        Raises
        ------
        
        InvalidOperandError
            if other is not a Fraction.
        """
        if not isinstance(other,Fraction):
            raise InvalidOperandError("can only add fraction to fraction")
        return Fraction(
            self._numerator * other._numerator,self._denominator * other._denominator
        )
    
    def reciprocal(self) -> "Fraction":
        """
        Return the reciprocal (multiplicative inverse) of this fraction.

        Returns
        -------
        Fraction
            A new Fraction with numerator and denominator swapped.

        Raises
        ------
        UndefinedOperationError
            If self.numerator is 0.
        """
        if self._numerator == 0:
            raise UndefinedOperationError("cannot take reciprocal of zero")
        return Fraction(self._denominator, self._numerator)

    def __truediv__(self,other:"Fraction")->"Fraction":
        """
        
        Divide this fraction by another
        
        (a/b) / (c/d) =(a*d)/(b*c)
        
        Parameters
        ----------
        other:Fraction
            the fraction to divide by.

        Return
        ------
        Fraction
            A new, simplified fraction representing the quotient.

        Raises
        ------
        InvalidOperandError
            if other is not a fraction.
        UndefinedOperationError
            if the other is zero
        """

        if not isinstance(other,Fraction):
            raise InvalidOperandError("can only add fraction to fraction")
        if other._numerator==0:
            raise UndefinedOperationError("cannot be divided by zero")
        return Fraction(
            self._numerator * other._denominator,self._denominator * other._numerator
        )

    def __eq__(self,other:"Fraction")->bool:
        """
        Check equality with another Fraction.

        Since both operands are stored in simplified form,equality is just numerator == numerator and denominator == denominator.

        Parameters
        ----------
        other : object
            The object to compare against.

        Returns
        -------
        bool
            True if other is a Fraction with the same simplified numerator and denominator. Returns NotImplemented (not False) if other is not a Fraction, so Python can fall back to other's __eq__ correctly.
        """

        if not isinstance(other,Fraction):
            return NotImplemented
        return self._numerator == other._numerator and self._denominator == other._denominator

    def __hash__(self)->int:
        """
        return a hash consistent with __eq__.
        
        Returns
        -------
        int 
            hash of (numerator,denominator).Required because defining __eq__ without __hash__ make the class unhashable - needed if fraction are ever used in a set ot as a dict key.
        """
        return hash((self._numerator, self._denominator))

    def to_float(self) ->float:
        """
        convert the fraction to float approximation.
        
        Returns
        -------
        float
            numerator / denominator as a Python float.
        """
        return self._numerator / self._denominator

    def __neg__(self)->"Fraction":
        """
        Return the negation of this fraction.
        
        Returns
        -------
        Fraction
            A new Fraction with the numerator's sign flipped.
        """
        return Fraction(
            -self._numerator ,self._denominator 
        ) 

    def __abs__(self) -> "Fraction":
        """
        Return the absolute value of this fraction.

        Returns
        -------
        Fraction
            A new Fraction with a non-negative numerator.
        """
        return Fraction(abs(self._numerator), self._denominator)


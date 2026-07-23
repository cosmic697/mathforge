"""
mathforge/arithmetic/numbers/decimal.py

Decimal 

Represents an exact fixed-point decimal number : unscaled_value * 10^exponent.
"""
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError

def _round_div(numerator : int, denominator : int)->int:
    """
    Integer division of numerator/denominator , round half-up , correct for negative numbers. used internally by __truediv__.
    """

    negative = (numerator < 0)!= (denominator < 0)
    numerator , denominator = abs(numerator),abs(denominator)
    quotient , remainder = divmod(numerator,denominator)
    if remainder *2 >= denominator:
        quotient+=1
    return -quotient if negative else quotient


class Decimal:
    """
    
    An exact fixed point decimal number.
     
    Internally stored as an integer "unscaled" value and an integer 'exponent' , such that the value is :
        unscaled * 10^exponent
        
    Decimal is deliberately NOT constructed from float. Floats cannot exactly represent most decimal fraction- which is precisely the problem a decimal type exist to avoid. Construct from a string or an int instead.
     
    Decimal instances are immutable - every operation returns a new Decimal.
    """

    DIVISION_EXTRA_DIGITS: int = 10

    def __init__(self,value):
        """
        Construct a Decimal from a string or an int.

        Parameters
        ----------
        value: str or int 
        
        Raises
        ------
        InvalidOperandError
            if a value is a float ,bool ot a string that isn't a valid decimal number.
        """
        if isinstance(value, bool):
            raise InvalidOperandError("Decimal cannot be constructed from a boolean.")

        if isinstance(value, float):
            raise InvalidOperandError(
                "Decimal cannot be constructed from a float, since floats "
                "cannot exactly represent most decimal fractions. "
                "Use a string instead, e.g. Decimal('3.14')."
            )

        if isinstance(value, int):
            self._unscaled = value
            self._exponent = 0
            return

        if isinstance(value, str):
            self._unscaled, self._exponent = self._parse(value)
            return

        raise InvalidOperandError("Decimal must be constructed from a str or an int.")

    @staticmethod
    def _parse(value: str):
        s = value.strip()
        negative = False
        if s[:1] in ("+", "-"):
            negative = s[0] == "-"
            s = s[1:]

        if "." in s:
            int_part, frac_part = s.split(".", 1)
        else:
            int_part, frac_part = s, ""

        if (int_part and not int_part.isdigit()) or (frac_part and not frac_part.isdigit()):
            raise InvalidOperandError(f"'{value}' is not a valid decimal string.")
        if not int_part and not frac_part:
            raise InvalidOperandError(f"'{value}' is not a valid decimal string.")

        digits = (int_part or "0") + frac_part
        unscaled = int(digits)
        if negative:
            unscaled = -unscaled

        exponent = -len(frac_part)
        return unscaled, exponent
        

    
    @classmethod
    def _from_unscaled(cls, unscaled: int,exponent:int)->"Decimal":
        """
        Internal constructor: build a decimal directly from an already-known unscaled value and exponent , skipping string parsing. used by arithmetic methods , which compute the results unscaled/exponent directly than building and reparsing a string.

        Parameters
        ----------
        unscaled : int
        exponent : int

        Returns
        -------
        Decimal 
        """
        obj = cls(0)
        obj._unscaled = unscaled
        obj._exponent = exponent
        return obj

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            In the form "Decimal('value')".
        """
        return f"Decimal('{str(self)}')"

    def __str__(self) -> str:
        """
        Returns
        -------
        str
            The plain decimal string, e.g. "3.14", "-0.50", "10".
        """
        if self._exponent >= 0:
            return str(self._unscaled * (10 ** self._exponent))

        scale = -self._exponent
        digits = str(abs(self._unscaled)).zfill(scale + 1)
        int_part, frac_part = digits[:-scale], digits[-scale:]
        sign = "-" if self._unscaled < 0 else ""
        return f"{sign}{int_part}.{frac_part}"


    def _aligned(self, other: "Decimal"):
        """Return (self_unscaled, other_unscaled, common_exponent)."""
        exponent = min(self._exponent, other._exponent)
        a = self._unscaled * 10 ** (self._exponent - exponent)
        b = other._unscaled * 10 ** (other._exponent - exponent)
        return a, b, exponent
        

    def __add__(self, other: "Decimal") -> "Decimal":
        """
        Add two Decimals.

        Since the two operands may have different exponents (e.g.
        "1.1" has exponent -1, "2.22" has exponent -2), both are
        first rescaled to the smaller (finer) of the two exponents
        before adding — the same way you'd line up decimal points
        by hand before adding on paper.

        Parameters
        ----------
        other : Decimal

        Returns
        -------
        Decimal

        Raises
        ------
        InvalidOperandError
            If other is not a Decimal.
        """
        if not isinstance(other, Decimal):
            raise InvalidOperandError("can only add Decimal to Decimal")
        a, b, exponent = self._aligned(other)
        return Decimal._from_unscaled(a + b, exponent)


    def __sub__(self, other: "Decimal") -> "Decimal":
        """
        Subtract another Decimal from this one. Same exponent-
        alignment approach as __add__.

        Parameters
        ----------
        other : Decimal

        Returns
        -------
        Decimal

        Raises
        ------
        InvalidOperandError
            If other is not a Decimal.
        """
        if not isinstance(other, Decimal):
            raise InvalidOperandError("can only subtract Decimal from Decimal")
        a, b, exponent = self._aligned(other)
        return Decimal._from_unscaled(a - b, exponent)


    def __mul__(self, other: "Decimal") -> "Decimal":
        """
        Multiply two Decimals.

        No alignment needed: unscaled values multiply directly,
        and exponents simply add (10^a * 10^b = 10^(a+b)).

        Parameters
        ----------
        other : Decimal

        Returns
        -------
        Decimal

        Raises
        ------
        InvalidOperandError
            If other is not a Decimal.
        """
        if not isinstance(other, Decimal):
            raise InvalidOperandError("can only multiply Decimal by Decimal")
        return Decimal._from_unscaled(
            self._unscaled * other._unscaled,
            self._exponent + other._exponent,
        )

    def __truediv__(self, other: "Decimal") -> "Decimal":
        """
        Divide this Decimal by another.

        Division can produce a non-terminating decimal (e.g. 1/3),
        so the result is computed to DIVISION_EXTRA_DIGITS extra
        digits of precision beyond the operands, then rounded
        (round-half-up) to that precision — it is NOT exact in
        general, unlike +, -, and *.

        Parameters
        ----------
        other : Decimal

        Returns
        -------
        Decimal

        Raises
        ------
        InvalidOperandError
            If other is not a Decimal.
        UndefinedOperationError
            If other is zero.
        """
        if not isinstance(other, Decimal):
            raise InvalidOperandError("can only divide Decimal by Decimal")
        if other._unscaled == 0:
            raise UndefinedOperationError("cannot divide by zero")

        exponent = self._exponent - other._exponent - self.DIVISION_EXTRA_DIGITS
        numerator = self._unscaled * (10 ** self.DIVISION_EXTRA_DIGITS)
        unscaled = _round_div(numerator, other._unscaled)
        return Decimal._from_unscaled(unscaled, exponent)


    def __eq__(self, other: object) -> bool:
        """
        Check equality with another Decimal.

        Aligns exponents first (same as __add__) so that
        Decimal("1.50") == Decimal("1.5") is True, even though
        they're stored with different exponents.

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            NotImplemented if other is not a Decimal.
        """
        if not isinstance(other, Decimal):
            return NotImplemented
        a, b, _ = self._aligned(other)
        return a == b

    def to_float(self) -> float:
        """
        Convert to a float approximation.

        Returns
        -------
        float
        """
        return self._unscaled * (10.0 ** self._exponent)

    def __neg__(self) -> "Decimal":
        """
        Returns
        -------
        Decimal
            A new Decimal with the unscaled value's sign flipped.
        """
        return Decimal._from_unscaled(-self._unscaled, self._exponent)

    def __abs__(self) -> "Decimal":
        """
        Returns
        -------
        Decimal
            A new Decimal with a non-negative unscaled value.
        """
        return Decimal._from_unscaled(abs(self._unscaled), self._exponent)
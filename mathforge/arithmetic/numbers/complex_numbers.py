"""
mathforge/arithmetic/numbers/complex_number.py

ComplexNumber

Represents a complex number as real + imag*i.
"""
from mathforge.core.constants import EPSILON
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError
import math


class ComplexNumber:
    """
    A complex number, represented as real + imag*i.

    ComplexNumber instances are immutable - every arithmetic operation
    returns a new ComplexNumber rather than modifying self. Equality
    uses a tolerance (EPSILON) since real/imag are stored as floats.

    Attributes
    ----------
    real : float
        The real part (read-only).
    imag : float
        The imaginary part (read-only).

    Examples
    --------
    >>> ComplexNumber(3, 4)
    ComplexNumber(3.0, 4.0)
    >>> ComplexNumber(1, 2) + ComplexNumber(3, -1)
    ComplexNumber(4.0, 1.0)
    """

    # Tolerance-based equality means two "equal" values can still
    # hash differently — so this class is intentionally unhashable
    # until something concrete needs it.
    __hash__ = None

    def __init__(self, real: float, imag: float = 0.0):
        """
        Construct a ComplexNumber.

        Parameters
        ----------
        real : float
            The real part. int is also accepted and converted to float.
        imag : float, optional
            The imaginary part. Defaults to 0.0, so ComplexNumber(3)
            represents the purely real number 3 + 0i.

        Raises
        ------
        InvalidOperandError
            If real or imag is not an int/float, or is a bool.
        """

        # reject if boolean
        if isinstance(real, bool) or isinstance(imag, bool):
            raise InvalidOperandError("real and imag must be numbers, not booleans.")

        # validate type
        if not isinstance(real, (int, float)) or not isinstance(imag, (int, float)):
            raise InvalidOperandError("real and imag must be int or float.")

        # declaring variables
        self._real = float(real)
        self._imag = float(imag)

    @property
    def real(self) -> float:
        """
        float: the real part
        """
        return self._real

    @property
    def imag(self) -> float:
        """
        float: the imag part
        """
        return self._imag

    def __repr__(self) -> str:
        """
        Return the unambiguous developer representation.

        Returns
        -------
        str
            In the form "ComplexNumber(real, imag)".
        """
        return f"ComplexNumber({self._real}, {self._imag})"

    def __str__(self) -> str:
        """
        Return the human-readable string form.

        Returns
        -------
        str
            In the form "real + imagi" or "real - imagi" depending
            on the sign of imag.
        """
        sign = "+" if self._imag >= 0 else "-"
        return f"{self._real} {sign} {abs(self._imag)}i"

    def __add__(self, other: "ComplexNumber") -> "ComplexNumber":
        """
        Add two complex numbers.

        (a+bi) + (c+di) = (a+c) + (b+d)i

        Parameters
        ----------
        other : ComplexNumber

        Returns
        -------
        ComplexNumber

        Raises
        ------
        InvalidOperandError
            If other is not a ComplexNumber.
        """
        if not isinstance(other, ComplexNumber):
            raise InvalidOperandError("can only add ComplexNumber to ComplexNumber")
        return ComplexNumber(self._real + other._real, self._imag + other._imag)

    def __sub__(self, other: "ComplexNumber") -> "ComplexNumber":
        """
        Subtract another complex number from this one.

        (a+bi) - (c+di) = (a-c) + (b-d)i

        Parameters
        ----------
        other : ComplexNumber

        Returns
        -------
        ComplexNumber

        Raises
        ------
        InvalidOperandError
            If other is not a ComplexNumber.
        """
        if not isinstance(other, ComplexNumber):
            raise InvalidOperandError("can only subtract ComplexNumber from ComplexNumber")
        return ComplexNumber(self._real - other._real, self._imag - other._imag)

    def __mul__(self, other: "ComplexNumber") -> "ComplexNumber":
        """
        Multiply two complex numbers.

        (a+bi) * (c+di) = (ac - bd) + (ad + bc)i

        Parameters
        ----------
        other : ComplexNumber

        Returns
        -------
        ComplexNumber

        Raises
        ------
        InvalidOperandError
            If other is not a ComplexNumber.
        """
        if not isinstance(other, ComplexNumber):
            raise InvalidOperandError("can only multiply ComplexNumber by ComplexNumber")
        real = self._real * other._real - self._imag * other._imag
        imag = self._real * other._imag + self._imag * other._real
        return ComplexNumber(real, imag)

    def __truediv__(self, other: "ComplexNumber") -> "ComplexNumber":
        """
        Divide this complex number by another.

        (a+bi) / (c+di) = ((ac+bd) + (bc-ad)i) / (c^2 + d^2)

        Parameters
        ----------
        other : ComplexNumber

        Returns
        -------
        ComplexNumber

        Raises
        ------
        InvalidOperandError
            If other is not a ComplexNumber.
        UndefinedOperationError
            If other is zero (real == 0 and imag == 0).
        """
        if not isinstance(other, ComplexNumber):
            raise InvalidOperandError("can only divide ComplexNumber by ComplexNumber")
        denom = other._real ** 2 + other._imag ** 2
        if denom == 0:
            raise UndefinedOperationError("cannot divide by zero ComplexNumber")
        real = (self._real * other._real + self._imag * other._imag) / denom
        imag = (self._imag * other._real - self._real * other._imag) / denom
        return ComplexNumber(real, imag)

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another ComplexNumber, within EPSILON tolerance.

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            True if other is a ComplexNumber whose real and imag
            parts are each within EPSILON of self's. Returns
            NotImplemented if other is not a ComplexNumber.
        """
        if not isinstance(other, ComplexNumber):
            return NotImplemented
        return (
            abs(self._real - other._real) < EPSILON
            and abs(self._imag - other._imag) < EPSILON
        )

    def conjugate(self) -> "ComplexNumber":
        """
        Return the complex conjugate.

        Returns
        -------
        ComplexNumber
            A new ComplexNumber with imag negated.
        """
        return ComplexNumber(self._real, -self._imag)

    def magnitude(self) -> float:
        """
        Return the magnitude (modulus) of this complex number.

        Returns
        -------
        float
            sqrt(real^2 + imag^2)
        """
        return math.sqrt(self._real ** 2 + self._imag ** 2)

    def __neg__(self) -> "ComplexNumber":
        """
        Return the negation of this complex number.

        Returns
        -------
        ComplexNumber
            A new ComplexNumber with both real and imag sign-flipped.
        """
        return ComplexNumber(-self._real, -self._imag)

    def __abs__(self) -> float:
        """
        Return the absolute value (magnitude) of this complex number.

        Returns
        -------
        float
            Same as self.magnitude(). Note this returns a float,
            not a ComplexNumber — unlike Fraction.__abs__.
        """
        return self.magnitude()
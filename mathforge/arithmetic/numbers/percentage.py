"""
mathforge/arithmetic/numbers/percentage.py

Percentage

Represents a percentage as an underlying ratio, backed by Fraction
for exactness (e.g. 50% is stored internally as Fraction(1, 2)).
"""

from mathforge.arithmetic.numbers.fraction import Fraction
from mathforge.core.errors import InvalidOperandError


class Percentage:
    """
    A percentage, backed internally by a Fraction ratio.

    A Percentage does NOT store "50" — it stores the ratio 50/100,
    simplified via Fraction, so it's exact and composes cleanly
    with the rest of the Arithmetic module.

    Percentage instances are immutable.

    Examples
    --------
    >>> Percentage.from_percent(50)
    Percentage(1/2)
    >>> Percentage.from_percent(20).apply_to(Fraction(50, 1))
    Fraction(10, 1)
    """

    def __init__(self, ratio: Fraction):
        """
        Construct a Percentage directly from an underlying ratio.

        Parameters
        ----------
        ratio : Fraction
            The underlying ratio (e.g. Fraction(1, 2) for 50%).

        Raises
        ------
        InvalidOperandError
            If ratio is not a Fraction.
        """
        if not isinstance(ratio, Fraction):
            raise InvalidOperandError("Percentage must be constructed from a Fraction ratio.")
        self._ratio = ratio

    @classmethod
    def from_percent(cls, value) -> "Percentage":
        """
        Construct a Percentage from a percent number.

        e.g. Percentage.from_percent(50) means "50 percent",
        stored internally as the ratio Fraction(50, 100) = Fraction(1, 2).

        Parameters
        ----------
        value : int or Fraction
            The percent value.

        Returns
        -------
        Percentage

        Raises
        ------
        InvalidOperandError
            If value is not an int or Fraction (or is a bool).
        """
        if isinstance(value, bool):
            raise InvalidOperandError("value must be an int or Fraction, not a boolean.")

        if isinstance(value, int):
            return cls(Fraction(value, 100))

        if isinstance(value, Fraction):
            return cls(value / Fraction(100, 1))

        raise InvalidOperandError("value must be an int or Fraction.")

    @property
    def ratio(self) -> Fraction:
        """
        Fraction: The underlying ratio (e.g. Fraction(1, 2) for 50%).
        """
        return self._ratio

    def to_percent(self) -> Fraction:
        """
        Return the percent-number form of this ratio.

        e.g. a Percentage with ratio Fraction(1, 2) returns Fraction(50, 1).

        Returns
        -------
        Fraction
        """
        return self._ratio * Fraction(100, 1)

    def apply_to(self, amount: Fraction) -> Fraction:
        """
        Apply this percentage to an amount.

        e.g. Percentage.from_percent(20).apply_to(Fraction(50, 1))
        returns Fraction(10, 1) — 20% of 50 is 10.

        Parameters
        ----------
        amount : Fraction

        Returns
        -------
        Fraction

        Raises
        ------
        InvalidOperandError
            If amount is not a Fraction.
        """
        if not isinstance(amount, Fraction):
            raise InvalidOperandError("amount must be a Fraction.")
        return self._ratio * amount

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            In the form "Percentage(numerator/denominator)".
        """
        return f"Percentage({self._ratio.numerator}/{self._ratio.denominator})"

    def __str__(self) -> str:
        """
        Returns
        -------
        str
            The percent-number form as a string with a % sign,
            e.g. "50%", or "33.33%" if not a whole number.
        """
        percent = self.to_percent()
        if percent.denominator == 1:
            return f"{percent.numerator}%"
        return f"{percent.to_float():.2f}%"

    def __add__(self, other: "Percentage") -> "Percentage":
        """
        Add two percentages (ratios add directly).

        Parameters
        ----------
        other : Percentage

        Returns
        -------
        Percentage

        Raises
        ------
        InvalidOperandError
            If other is not a Percentage.
        """
        if not isinstance(other, Percentage):
            raise InvalidOperandError("can only add Percentage to Percentage")
        return Percentage(self._ratio + other._ratio)

    def __sub__(self, other: "Percentage") -> "Percentage":
        """
        Subtract two percentages (ratios subtract directly).

        Parameters
        ----------
        other : Percentage

        Returns
        -------
        Percentage

        Raises
        ------
        InvalidOperandError
            If other is not a Percentage.
        """
        if not isinstance(other, Percentage):
            raise InvalidOperandError("can only subtract Percentage from Percentage")
        return Percentage(self._ratio - other._ratio)

    def __eq__(self, other: object) -> bool:
        """
        Check equality via the underlying ratio.

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            NotImplemented if other is not a Percentage.
        """
        if not isinstance(other, Percentage):
            return NotImplemented
        return self._ratio == other._ratio

    def __hash__(self) -> int:
        """
        Returns
        -------
        int
            Hash of the underlying ratio.
        """
        return hash(self._ratio)
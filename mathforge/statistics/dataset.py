"""
mathforge/statistics/dataset.py

Dataset

Represents a collection of numeric observations, with descriptive statistics (mean, median, mode, variance, standard deviation).
"""

import math
from collections import Counter

from mathforge.core.errors import InvalidOperandError, UndefinedOperationError


class Dataset:
    """
    An immutable collection of numeric observations.

    Attributes
    ----------
    values : tuple of float
        The observations (read-only).

    Examples
    --------
    >>> d = Dataset([2, 4, 4, 4, 5, 5, 7, 9])
    >>> d.mean()
    5.0
    >>> d.mode()
    (4.0,)
    """

    def __init__(self, values):
        """
        Construct a Dataset from a sequence of numbers.

        Parameters
        ----------
        values : sequence of int/float
            Must be non-empty. Each element is converted to float.

        Raises
        ------
        InvalidOperandError
            If values is empty, not a sequence, or contains a non-numeric or boolean element.
        """
        if isinstance(values, (str, bytes)):
            raise InvalidOperandError("values must be a sequence of numbers, not a string.")

        try:
            items = list(values)
        except TypeError:
            raise InvalidOperandError("values must be an iterable sequence of numbers.")

        if len(items) == 0:
            raise InvalidOperandError("Dataset must have at least one value.")

        converted = []
        for item in items:
            if isinstance(item, bool):
                raise InvalidOperandError("values must be numbers, not booleans.")
            if not isinstance(item, (int, float)):
                raise InvalidOperandError("values must be int or float.")
            converted.append(float(item))

        self._values = tuple(converted)

    @property
    def values(self) -> tuple:
        """tuple of float: The observations."""
        return self._values

    def __len__(self) -> int:
        """
        Returns
        -------
        int
            Number of observations.
        """
        return len(self._values)

    def mean(self) -> float:
        """
        Return the arithmetic mean.

        Returns
        -------
        float
        """
        return sum(self._values) / len(self._values)

    def median(self) -> float:
        """
        Return the median.

        For an odd number of observations, the middle value after sorting. For an even number, the average of the two middle values.

        Returns
        -------
        float
        """
        sorted_values = sorted(self._values)
        n = len(sorted_values)
        mid = n // 2
        if n % 2 == 1:
            return sorted_values[mid]
        return (sorted_values[mid - 1] + sorted_values[mid]) / 2

    def mode(self) -> tuple:
        """
        Return the mode(s): the most frequently occurring value(s).

        If multiple values are tied for the highest frequency, all of them are returned (in ascending order) rather than arbitrarily picking one — a tie is a real feature of the data, not something to silently resolve.

        Returns
        -------
        tuple of float
            One or more values, ascending order.
        """
        counts = Counter(self._values)
        highest = max(counts.values())
        return tuple(sorted(v for v, c in counts.items() if c == highest))

    def variance(self, sample: bool = True) -> float:
        """
        Return the variance.

        Parameters
        ----------
        sample : bool, optional
            If True (default), computes sample variance (divides by n - 1, Bessel's correction — the standard choice when this data is a sample used to estimate a larger population's variance). If False, computes population variance (divides by n — use only when this dataset IS the entire population being studied, not a sample of it).

        Returns
        -------
        float

        Raises
        ------
        UndefinedOperationError
            If sample=True and there is only one observation (n - 1 would be zero, making the division undefined).
        """
        n = len(self._values)
        if sample and n < 2:
            raise UndefinedOperationError(
                "sample variance is undefined for a dataset with fewer than 2 values"
            )
        mean = self.mean()
        squared_diffs = sum((x - mean) ** 2 for x in self._values)
        divisor = (n - 1) if sample else n
        return squared_diffs / divisor

    def std_dev(self, sample: bool = True) -> float:
        """
        Return the standard deviation (square root of variance).

        Parameters
        ----------
        sample : bool, optional
            Same meaning as in variance(). Defaults to True.

        Returns
        -------
        float

        Raises
        ------
        UndefinedOperationError
            Same condition as variance().
        """
        return math.sqrt(self.variance(sample=sample))

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            In the form "Dataset(1.0, 2.0, 3.0)".
        """
        inner = ", ".join(str(v) for v in self._values)
        return f"Dataset({inner})"
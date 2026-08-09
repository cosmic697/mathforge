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

    def covariance(self, other: "Dataset", sample: bool = True) -> float:
        """
        Return the covariance between this dataset and another.

        Measures how two variables change together: positive means
        they tend to increase together, negative means one tends
        to increase as the other decreases, near zero means little
        linear relationship.

        cov = sum((x_i - mean_x) * (y_i - mean_y)) / divisor

        Parameters
        ----------
        other : Dataset
            Must have the same number of observations as self —
            covariance is defined on paired observations (e.g.
            (height_i, weight_i) for the same person i), not on
            two unrelated collections of different sizes.
        sample : bool, optional
            Same n-1 vs n choice as Dataset.variance(). Defaults
            to True (sample covariance).

        Returns
        -------
        float

        Raises
        ------
        InvalidOperandError
            If other is not a Dataset, or the two datasets have
            different lengths.
        UndefinedOperationError
            If sample=True and there are fewer than 2 paired
            observations.
        """
        if not isinstance(other, Dataset):
            raise InvalidOperandError("can only compute covariance with another Dataset")
        if len(self) != len(other):
            raise InvalidOperandError(
                f"covariance requires paired observations of equal length "
                f"({len(self)} vs {len(other)})"
            )

        n = len(self)
        if sample and n < 2:
            raise UndefinedOperationError(
                "sample covariance is undefined for fewer than 2 paired observations"
            )

        mean_x = self.mean()
        mean_y = other.mean()
        total = sum(
            (x - mean_x) * (y - mean_y)
            for x, y in zip(self._values, other._values)
        )
        divisor = (n - 1) if sample else n
        return total / divisor

    def correlation(self, other: "Dataset") -> float:
        """
        Return the Pearson correlation coefficient with another
        dataset: covariance normalized by both standard deviations,
        always in the range [-1, 1].

        correlation = covariance(x, y) / (std_dev(x) * std_dev(y))

        A value near 1 means a strong positive linear relationship,
        near -1 a strong negative one, near 0 little linear
        relationship (note: NOT "no relationship" — correlation
        only captures LINEAR relationships; two variables can be
        strongly related in a non-linear way and still show
        correlation near 0).

        Parameters
        ----------
        other : Dataset
            Must have the same number of observations as self.

        Returns
        -------
        float

        Raises
        ------
        InvalidOperandError
            If other is not a Dataset, or lengths differ.
        UndefinedOperationError
            If either dataset has zero variance (all identical
            values) — correlation is undefined when there's no
            spread to normalize against (division by zero).
        """
        std_x = self.std_dev(sample=True)
        std_y = other.std_dev(sample=True)
        if std_x == 0 or std_y == 0:
            raise UndefinedOperationError(
                "correlation is undefined when either dataset has zero variance"
            )
        return self.covariance(other, sample=True) / (std_x * std_y)

    def linear_regression(self, other: "Dataset") -> tuple:
        """
        Compute the simple linear regression of other (y) on self (x):
        the line y = slope * x + intercept that best fits the paired
        observations, in the least-squares sense.

        slope = covariance(x, y) / variance(x)
        intercept = mean(y) - slope * mean(x)

        Parameters
        ----------
        other : Dataset
            The dependent variable (y). Must have the same number
            of observations as self (the independent variable, x).

        Returns
        -------
        tuple of (float, float)
            (slope, intercept).

        Raises
        ------
        InvalidOperandError
            If other is not a Dataset, or lengths differ.
        UndefinedOperationError
            If self (x) has zero variance — a vertical-line fit
            has no defined slope in this y = mx + b form.
        """
        var_x = self.variance(sample=True)
        if var_x == 0:
            raise UndefinedOperationError(
                "linear regression is undefined when the independent variable has zero variance"
            )
        slope = self.covariance(other, sample=True) / var_x
        intercept = other.mean() - slope * self.mean()
        return (slope, intercept)
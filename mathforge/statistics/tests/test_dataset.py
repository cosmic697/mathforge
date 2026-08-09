"""
mathforge/statistics/tests/test_dataset.py

Unit tests for the Dataset class.
"""

import pytest

from mathforge.statistics.dataset import Dataset
from mathforge.core.errors import InvalidOperandError, UndefinedOperationError


# --- Construction ---

def test_construct_basic():
    d = Dataset([1, 2, 3])
    assert d.values == (1.0, 2.0, 3.0)


def test_construct_single_value():
    d = Dataset([5])
    assert len(d) == 1


def test_construct_empty_raises():
    with pytest.raises(InvalidOperandError):
        Dataset([])


def test_construct_rejects_string():
    with pytest.raises(InvalidOperandError):
        Dataset("123")


def test_construct_rejects_bool():
    with pytest.raises(InvalidOperandError):
        Dataset([1, True, 3])


def test_construct_rejects_non_numeric():
    with pytest.raises(InvalidOperandError):
        Dataset([1, "2", 3])


# --- len / repr ---

def test_len():
    assert len(Dataset([1, 2, 3, 4])) == 4


def test_repr():
    assert repr(Dataset([1, 2, 3])) == "Dataset(1.0, 2.0, 3.0)"


# --- mean ---

def test_mean():
    assert Dataset([2, 4, 6]).mean() == 4.0


def test_mean_single_value():
    assert Dataset([7]).mean() == 7.0


# --- median ---

def test_median_odd_count():
    assert Dataset([3, 1, 2]).median() == 2.0


def test_median_even_count():
    assert Dataset([1, 2, 3, 4]).median() == 2.5


def test_median_unsorted_input():
    assert Dataset([5, 1, 3, 2, 4]).median() == 3.0


# --- mode ---

def test_mode_single_winner():
    assert Dataset([2, 4, 4, 4, 5, 5, 7, 9]).mode() == (4.0,)


def test_mode_tie():
    assert Dataset([1, 1, 2, 2, 3]).mode() == (1.0, 2.0)


def test_mode_all_unique_returns_all():
    assert Dataset([1, 2, 3]).mode() == (1.0, 2.0, 3.0)


# --- variance ---

def test_sample_variance():
    # [2, 4, 4, 4, 5, 5, 7, 9], mean=5, known sample variance = 4.571428...
    d = Dataset([2, 4, 4, 4, 5, 5, 7, 9])
    assert abs(d.variance(sample=True) - 4.571428571428571) < 1e-9


def test_population_variance():
    # same data, known population variance = 4.0
    d = Dataset([2, 4, 4, 4, 5, 5, 7, 9])
    assert abs(d.variance(sample=False) - 4.0) < 1e-9


def test_sample_variance_single_value_raises():
    with pytest.raises(UndefinedOperationError):
        Dataset([5]).variance(sample=True)


def test_population_variance_single_value_is_zero():
    assert Dataset([5]).variance(sample=False) == 0.0


def test_variance_defaults_to_sample():
    d = Dataset([2, 4, 4, 4, 5, 5, 7, 9])
    assert d.variance() == d.variance(sample=True)


# --- std_dev ---

def test_sample_std_dev():
    d = Dataset([2, 4, 4, 4, 5, 5, 7, 9])
    assert abs(d.std_dev(sample=True) - math.sqrt(4.571428571428571)) < 1e-9


def test_population_std_dev():
    d = Dataset([2, 4, 4, 4, 5, 5, 7, 9])
    assert abs(d.std_dev(sample=False) - 2.0) < 1e-9


import math 

# --- covariance ---

def test_covariance_positive_relationship():
    x = Dataset([1, 2, 3, 4, 5])
    y = Dataset([2, 4, 6, 8, 10])
    assert abs(x.covariance(y) - 5.0) < 1e-9


def test_covariance_rejects_non_dataset():
    with pytest.raises(InvalidOperandError):
        Dataset([1, 2, 3]).covariance([1, 2, 3])


def test_covariance_rejects_mismatched_length():
    with pytest.raises(InvalidOperandError):
        Dataset([1, 2, 3]).covariance(Dataset([1, 2]))


def test_covariance_single_pair_raises_for_sample():
    with pytest.raises(UndefinedOperationError):
        Dataset([1]).covariance(Dataset([2]), sample=True)


# --- correlation ---

def test_correlation_perfect_positive():
    x = Dataset([1, 2, 3, 4, 5])
    y = Dataset([2, 4, 6, 8, 10])
    assert abs(x.correlation(y) - 1.0) < 1e-9


def test_correlation_perfect_negative():
    x = Dataset([1, 2, 3, 4, 5])
    y = Dataset([10, 8, 6, 4, 2])
    assert abs(x.correlation(y) - (-1.0)) < 1e-9


def test_correlation_zero_variance_raises():
    x = Dataset([5, 5, 5, 5])
    y = Dataset([1, 2, 3, 4])
    with pytest.raises(UndefinedOperationError):
        x.correlation(y)


# --- linear_regression ---

def test_linear_regression_exact_line():
    # y = 2x, so slope=2, intercept=0
    x = Dataset([1, 2, 3, 4])
    y = Dataset([2, 4, 6, 8])
    slope, intercept = x.linear_regression(y)
    assert abs(slope - 2.0) < 1e-9
    assert abs(intercept - 0.0) < 1e-9


def test_linear_regression_with_intercept():
    # y = 2x + 1
    x = Dataset([1, 2, 3, 4])
    y = Dataset([3, 5, 7, 9])
    slope, intercept = x.linear_regression(y)
    assert abs(slope - 2.0) < 1e-9
    assert abs(intercept - 1.0) < 1e-9


def test_linear_regression_zero_variance_x_raises():
    x = Dataset([5, 5, 5])
    y = Dataset([1, 2, 3])
    with pytest.raises(UndefinedOperationError):
        x.linear_regression(y)
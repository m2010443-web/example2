"""Tests for analysis module."""

import pytest
import pandas as pd
import numpy as np
from src import analysis


def test_calculate_basic_stats():
    """Test basic statistics calculation."""
    df = pd.DataFrame({'values': [1, 2, 3, 4, 5]})
    
    stats = analysis.calculate_basic_stats(df, 'values')
    
    assert stats['mean'] == 3.0
    assert stats['median'] == 3.0
    assert stats['min'] == 1
    assert stats['max'] == 5


def test_calculate_correlation():
    """Test correlation calculation."""
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [2, 4, 6, 8, 10]
    })
    
    corr = analysis.calculate_correlation(df)
    
    assert corr.loc['A', 'B'] == pytest.approx(1.0, abs=0.01)


def test_group_and_aggregate():
    """Test grouping and aggregation."""
    df = pd.DataFrame({
        'category': ['A', 'A', 'B', 'B'],
        'values': [10, 20, 30, 40]
    })
    
    result = analysis.group_and_aggregate(df, 'category', 'values', 'sum')
    
    assert len(result) == 2
    assert result[result['category'] == 'A']['values'].values[0] == 30
    assert result[result['category'] == 'B']['values'].values[0] == 70

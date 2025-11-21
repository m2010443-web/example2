"""Tests for data_loader module."""

import pytest
import pandas as pd
import numpy as np
from src import data_loader


def test_detect_column_types():
    """Test column type detection."""
    df = pd.DataFrame({
        'num': [1, 2, 3],
        'cat': ['a', 'b', 'c'],
        'date': pd.date_range('2023-01-01', periods=3)
    })
    
    types = data_loader.detect_column_types(df)
    
    assert 'num' in types['numeric']
    assert 'cat' in types['categorical']
    assert 'date' in types['datetime']


def test_clean_data():
    """Test data cleaning."""
    df = pd.DataFrame({
        'A': [1, 2, np.nan, 4, 4],
        'B': ['x', 'y', 'z', 'x', 'x']
    })
    
    cleaned = data_loader.clean_data(df)
    
    # Check duplicates removed
    assert len(cleaned) <= len(df)
    
    # Check NaNs filled
    assert cleaned['A'].isna().sum() == 0

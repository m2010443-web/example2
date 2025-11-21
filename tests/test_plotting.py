"""Tests for plotting module."""

import pytest
import pandas as pd
from src import plotting


def test_create_line_chart():
    """Test line chart creation."""
    df = pd.DataFrame({
        'x': [1, 2, 3],
        'y': [10, 20, 30]
    })
    
    fig = plotting.create_line_chart(df, 'x', 'y')
    
    assert fig is not None
    assert len(fig.data) > 0


def test_create_bar_chart():
    """Test bar chart creation."""
    df = pd.DataFrame({
        'category': ['A', 'B', 'C'],
        'values': [10, 20, 30]
    })
    
    fig = plotting.create_bar_chart(df, 'category', 'values')
    
    assert fig is not None
    assert len(fig.data) > 0

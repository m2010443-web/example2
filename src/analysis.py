"""Data analysis module."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple


def calculate_basic_stats(df: pd.DataFrame, column: str) -> Dict:
    """Calculate basic statistics for a column."""
    stats = {
        'mean': df[column].mean(),
        'median': df[column].median(),
        'std': df[column].std(),
        'min': df[column].min(),
        'max': df[column].max(),
        'q25': df[column].quantile(0.25),
        'q75': df[column].quantile(0.75)
    }
    return stats


def calculate_correlation(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Calculate correlation matrix."""
    if columns:
        return df[columns].corr()
    return df.select_dtypes(include=['number']).corr()


def group_and_aggregate(df: pd.DataFrame, group_by: str, agg_column: str, 
                        agg_func: str = 'sum') -> pd.DataFrame:
    """Group data and aggregate."""
    return df.groupby(group_by)[agg_column].agg(agg_func).reset_index()


def detect_outliers(df: pd.DataFrame, column: str, method: str = 'iqr') -> pd.Series:
    """Detect outliers in a column."""
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (df[column] < lower_bound) | (df[column] > upper_bound)
    return pd.Series([False] * len(df))

"""Data loading and preprocessing module."""

import pandas as pd
import numpy as np
from typing import Optional, List, Tuple
from pathlib import Path


def load_csv(file_path: str) -> pd.DataFrame:
    """Load CSV file into DataFrame."""
    return pd.read_csv(file_path)


def load_excel(file_path: str, sheet_name: str = 0) -> pd.DataFrame:
    """Load Excel file into DataFrame."""
    return pd.read_excel(file_path, sheet_name=sheet_name)


def detect_column_types(df: pd.DataFrame) -> dict:
    """Detect column types in DataFrame."""
    types = {
        'numeric': df.select_dtypes(include=['number']).columns.tolist(),
        'categorical': df.select_dtypes(include=['object', 'category']).columns.tolist(),
        'datetime': df.select_dtypes(include=['datetime64']).columns.tolist()
    }
    return types


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean DataFrame."""
    df_clean = df.copy()
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # Fill numeric NaNs with median
    numeric_cols = df_clean.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    return df_clean

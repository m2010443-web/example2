#!/bin/bash

# Create all project files

# ==== requirements.txt ====
cat > requirements.txt << 'EOF'
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
openpyxl>=3.1.0
pytest>=7.4.0
pytest-cov>=4.1.0
EOF

# ==== .gitignore ====
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Data files
*.csv
*.xlsx
*.xls
!demo_data.py

# Streamlit
.streamlit/secrets.toml
EOF

# ==== .streamlit/config.toml ====
cat > .streamlit/config.toml << 'EOF'
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
EOF

# ==== src/__init__.py ====
cat > src/__init__.py << 'EOF'
"""
Sales Analytics Platform - Source Package
"""

from . import data_loader
from . import analysis
from . import plotting

__version__ = "3.0.0"
__all__ = ['data_loader', 'analysis', 'plotting']
EOF

# ==== src/data_loader.py ====
cat > src/data_loader.py << 'EOF'
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
EOF

# ==== src/analysis.py ====
cat > src/analysis.py << 'EOF'
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
EOF

# ==== src/plotting.py ====
cat > src/plotting.py << 'EOF'
"""Plotting and visualization module."""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, List


def create_line_chart(df: pd.DataFrame, x: str, y: str, 
                      title: Optional[str] = None) -> go.Figure:
    """Create a line chart."""
    fig = px.line(df, x=x, y=y, title=title or f"{y} over {x}")
    return fig


def create_bar_chart(df: pd.DataFrame, x: str, y: str, 
                     title: Optional[str] = None) -> go.Figure:
    """Create a bar chart."""
    fig = px.bar(df, x=x, y=y, title=title or f"{y} by {x}")
    return fig


def create_pie_chart(df: pd.DataFrame, names: str, values: str, 
                     title: Optional[str] = None) -> go.Figure:
    """Create a pie chart."""
    fig = px.pie(df, names=names, values=values, title=title or f"Distribution of {values}")
    return fig


def create_scatter_plot(df: pd.DataFrame, x: str, y: str, 
                        title: Optional[str] = None) -> go.Figure:
    """Create a scatter plot."""
    fig = px.scatter(df, x=x, y=y, title=title or f"{y} vs {x}")
    return fig


def create_correlation_heatmap(df: pd.DataFrame, 
                                title: Optional[str] = None) -> go.Figure:
    """Create correlation heatmap."""
    corr = df.select_dtypes(include=['number']).corr()
    fig = px.imshow(corr, title=title or "Correlation Heatmap", 
                    color_continuous_scale="RdBu")
    return fig
EOF

echo "All source files created successfully!"

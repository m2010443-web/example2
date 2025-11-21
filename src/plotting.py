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

"""
Demo Data Generator for Sales Analytics Platform
Generates realistic demo datasets for demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict


def generate_demo_data(n_records: int = 2000, seed: int = 42) -> pd.DataFrame:
    """
    Generate comprehensive demo sales data.
    
    Args:
        n_records: Number of records to generate
        seed: Random seed for reproducibility
        
    Returns:
        DataFrame with demo sales data
    """
    np.random.seed(seed)
    
    # Date range
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=int(x)) for x in np.sort(np.random.rand(n_records) * 365)]
    
    # Products
    products = ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Mouse', 'Keyboard', 
                'Monitor', 'Webcam', 'Speaker', 'Charger']
    product_list = np.random.choice(products, n_records, p=[0.15, 0.20, 0.12, 0.10, 0.08, 0.07, 0.13, 0.05, 0.06, 0.04])
    
    # Categories
    category_map = {
        'Laptop': 'Computers',
        'Phone': 'Mobile',
        'Tablet': 'Mobile',
        'Headphones': 'Accessories',
        'Mouse': 'Accessories',
        'Keyboard': 'Accessories',
        'Monitor': 'Computers',
        'Webcam': 'Accessories',
        'Speaker': 'Accessories',
        'Charger': 'Accessories'
    }
    categories = [category_map[p] for p in product_list]
    
    # Regions
    regions = ['North', 'South', 'East', 'West', 'Central']
    region_list = np.random.choice(regions, n_records, p=[0.22, 0.18, 0.25, 0.20, 0.15])
    
    # Sales channels
    channels = ['Online', 'Retail', 'Partner']
    channel_list = np.random.choice(channels, n_records, p=[0.45, 0.35, 0.20])
    
    # Customer segments
    segments = ['Enterprise', 'SMB', 'Consumer']
    segment_list = np.random.choice(segments, n_records, p=[0.25, 0.35, 0.40])
    
    # Base prices
    base_prices = {
        'Laptop': 1200, 'Phone': 800, 'Tablet': 500, 'Headphones': 150,
        'Mouse': 50, 'Keyboard': 80, 'Monitor': 350, 'Webcam': 100,
        'Speaker': 120, 'Charger': 30
    }
    
    # Generate prices with variation
    prices = [base_prices[p] * np.random.uniform(0.8, 1.2) for p in product_list]
    
    # Quantities (with seasonal patterns)
    month_multipliers = {1: 0.8, 2: 0.85, 3: 0.9, 4: 1.0, 5: 1.0, 6: 1.1,
                        7: 1.15, 8: 1.1, 9: 1.0, 10: 1.05, 11: 1.3, 12: 1.4}
    quantities = []
    for date in dates:
        base_qty = np.random.poisson(2) + 1
        seasonal = month_multipliers[date.month]
        quantities.append(int(base_qty * seasonal))
    
    # Calculate revenue
    revenue = [p * q for p, q in zip(prices, quantities)]
    
    # Costs (70-85% of price)
    costs = [p * np.random.uniform(0.70, 0.85) * q for p, q, in zip(prices, quantities)]
    
    # Profit
    profit = [r - c for r, c in zip(revenue, costs)]
    
    # Customer IDs
    n_customers = n_records // 3
    customer_ids = [f'CUST{i:05d}' for i in np.random.randint(1, n_customers + 1, n_records)]
    
    # Order IDs
    order_ids = [f'ORD{i:06d}' for i in range(1, n_records + 1)]
    
    # Sales reps
    reps = [f'Rep_{i:02d}' for i in range(1, 21)]
    rep_list = np.random.choice(reps, n_records)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Order_ID': order_ids,
        'Date': dates,
        'Customer_ID': customer_ids,
        'Product': product_list,
        'Category': categories,
        'Quantity': quantities,
        'Unit_Price': [round(p, 2) for p in prices],
        'Revenue': [round(r, 2) for r in revenue],
        'Cost': [round(c, 2) for c in costs],
        'Profit': [round(p, 2) for p in profit],
        'Region': region_list,
        'Channel': channel_list,
        'Customer_Segment': segment_list,
        'Sales_Rep': rep_list
    })
    
    return df


def generate_monthly_demo_data(seed: int = 42) -> pd.DataFrame:
    """Generate monthly aggregated demo data."""
    np.random.seed(seed)
    
    months = pd.date_range('2023-01', '2023-12', freq='MS')
    
    data = {
        'Month': months,
        'Total_Revenue': np.random.uniform(150000, 250000, 12),
        'Total_Orders': np.random.randint(400, 700, 12),
        'Avg_Order_Value': np.random.uniform(300, 500, 12),
        'Customer_Count': np.random.randint(300, 500, 12),
        'New_Customers': np.random.randint(50, 120, 12)
    }
    
    df = pd.DataFrame(data)
    df['Total_Revenue'] = df['Total_Revenue'].round(2)
    df['Avg_Order_Value'] = df['Avg_Order_Value'].round(2)
    
    return df


def generate_top_products_data(seed: int = 42) -> pd.DataFrame:
    """Generate top products demo data."""
    np.random.seed(seed)
    
    products = ['Laptop Pro', 'Smartphone X', 'Tablet Mini', 'Wireless Headphones', 
                'Gaming Mouse', 'Mechanical Keyboard', '4K Monitor', 'HD Webcam', 
                'Bluetooth Speaker', 'Fast Charger']
    
    data = {
        'Product': products,
        'Units_Sold': np.random.randint(500, 2000, 10),
        'Revenue': np.random.uniform(50000, 200000, 10),
        'Avg_Rating': np.random.uniform(3.5, 5.0, 10),
        'Return_Rate': np.random.uniform(1, 8, 10)
    }
    
    df = pd.DataFrame(data)
    df = df.sort_values('Revenue', ascending=False)
    df['Revenue'] = df['Revenue'].round(2)
    df['Avg_Rating'] = df['Avg_Rating'].round(1)
    df['Return_Rate'] = df['Return_Rate'].round(2)
    
    return df


def get_demo_datasets() -> Dict[str, pd.DataFrame]:
    """
    Get all demo datasets.
    
    Returns:
        Dictionary with dataset names as keys and DataFrames as values
    """
    return {
        "📊 Детальные продажи (2000 записей)": generate_demo_data(2000),
        "📅 Месячная статистика (12 месяцев)": generate_monthly_demo_data(),
        "🏆 Топ продукты (10 товаров)": generate_top_products_data()
    }


def get_demo_description() -> Dict[str, str]:
    """Get descriptions for demo datasets."""
    return {
        "📊 Детальные продажи (2000 записей)": 
            "Подробные данные о продажах с информацией о заказах, продуктах, регионах и каналах",
        "📅 Месячная статистика (12 месяцев)": 
            "Агрегированные месячные показатели выручки, заказов и клиентов за 2023 год",
        "🏆 Топ продукты (10 товаров)": 
            "Рейтинг самых популярных продуктов с метриками продаж и рейтингами"
    }


if __name__ == "__main__":
    # Test generation
    print("Generating demo data...")
    datasets = get_demo_datasets()
    
    for name, df in datasets.items():
        print(f"\n{name}")
        print(f"Shape: {df.shape}")
        print(df.head())

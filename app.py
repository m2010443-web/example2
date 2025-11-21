"""
Sales Analytics Platform - Standalone Version
All-in-one Streamlit application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import io

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# DEMO DATA FUNCTIONS
# ============================================================================

def generate_demo_data(n_records: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Generate comprehensive demo sales data."""
    np.random.seed(seed)
    
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=int(x)) for x in np.sort(np.random.rand(n_records) * 365)]
    
    products = ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Mouse', 'Keyboard', 
                'Monitor', 'Webcam', 'Speaker', 'Charger']
    product_list = np.random.choice(products, n_records, p=[0.15, 0.20, 0.12, 0.10, 0.08, 0.07, 0.13, 0.05, 0.06, 0.04])
    
    category_map = {
        'Laptop': 'Computers', 'Phone': 'Mobile', 'Tablet': 'Mobile',
        'Headphones': 'Accessories', 'Mouse': 'Accessories', 'Keyboard': 'Accessories',
        'Monitor': 'Computers', 'Webcam': 'Accessories', 'Speaker': 'Accessories', 'Charger': 'Accessories'
    }
    categories = [category_map[p] for p in product_list]
    
    regions = ['North', 'South', 'East', 'West', 'Central']
    region_list = np.random.choice(regions, n_records, p=[0.22, 0.18, 0.25, 0.20, 0.15])
    
    channels = ['Online', 'Retail', 'Partner']
    channel_list = np.random.choice(channels, n_records, p=[0.45, 0.35, 0.20])
    
    segments = ['Enterprise', 'SMB', 'Consumer']
    segment_list = np.random.choice(segments, n_records, p=[0.25, 0.35, 0.40])
    
    base_prices = {
        'Laptop': 1200, 'Phone': 800, 'Tablet': 500, 'Headphones': 150,
        'Mouse': 50, 'Keyboard': 80, 'Monitor': 350, 'Webcam': 100,
        'Speaker': 120, 'Charger': 30
    }
    
    prices = [base_prices[p] * np.random.uniform(0.8, 1.2) for p in product_list]
    
    month_multipliers = {1: 0.8, 2: 0.85, 3: 0.9, 4: 1.0, 5: 1.0, 6: 1.1,
                        7: 1.15, 8: 1.1, 9: 1.0, 10: 1.05, 11: 1.3, 12: 1.4}
    quantities = []
    for date in dates:
        base_qty = np.random.poisson(2) + 1
        seasonal = month_multipliers[date.month]
        quantities.append(int(base_qty * seasonal))
    
    revenue = [p * q for p, q in zip(prices, quantities)]
    costs = [p * np.random.uniform(0.70, 0.85) * q for p, q in zip(prices, quantities)]
    profit = [r - c for r, c in zip(revenue, costs)]
    
    n_customers = n_records // 3
    customer_ids = [f'CUST{i:05d}' for i in np.random.randint(1, n_customers + 1, n_records)]
    order_ids = [f'ORD{i:06d}' for i in range(1, n_records + 1)]
    
    reps = [f'Rep_{i:02d}' for i in range(1, 21)]
    rep_list = np.random.choice(reps, n_records)
    
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
    """Get all demo datasets."""
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


# ============================================================================
# SESSION STATE
# ============================================================================

def init_session_state():
    """Initialize session state variables."""
    if 'data' not in st.session_state:
        st.session_state['data'] = None
    if 'current_section' not in st.session_state:
        st.session_state['current_section'] = 'Загрузка данных'
    if 'data_source' not in st.session_state:
        st.session_state['data_source'] = None


# ============================================================================
# DATA LOADING SECTION
# ============================================================================

def load_data_section():
    """Data loading section with demo data support."""
    st.title("📊 Sales Analytics Platform")
    st.markdown("### 📁 Загрузка данных")
    
    uploaded_file = st.file_uploader(
        "Загрузите файл с данными о продажах",
        type=['csv', 'xlsx', 'xls'],
        help="Поддерживаются форматы: CSV, Excel (xlsx, xls)"
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner('Загрузка файла...'):
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                if file_extension == 'csv':
                    df = pd.read_csv(uploaded_file)
                elif file_extension in ['xlsx', 'xls']:
                    df = pd.read_excel(uploaded_file)
                else:
                    st.error("Неподдерживаемый формат файла")
                    return
                
                st.session_state['data'] = df
                st.session_state['data_source'] = 'uploaded'
                st.success(f"✅ Файл загружен! {len(df)} записей.")
                st.rerun()
                
        except Exception as e:
            st.error(f"Ошибка при загрузке файла: {str(e)}")
            st.info("Проверьте формат файла и попробуйте снова")
    
    st.markdown("---")
    st.markdown("### 🎬 Или попробуйте демо-данные")
    st.info("💡 Не хотите загружать файл? Попробуйте наши готовые датасеты!")
    
    demo_datasets = get_demo_datasets()
    dataset_descriptions = get_demo_description()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_demo = st.selectbox(
            "Выберите демо-датасет:",
            [""] + list(demo_datasets.keys()),
            format_func=lambda x: "Выберите..." if x == "" else x
        )
    
    with col2:
        st.write("")
        load_demo = st.button(
            "📊 Загрузить демо",
            type="primary",
            disabled=not selected_demo,
            use_container_width=True
        )
    
    if selected_demo and selected_demo in dataset_descriptions:
        st.caption(f"ℹ️ {dataset_descriptions[selected_demo]}")
    
    if load_demo and selected_demo:
        with st.spinner(f'Загружаю {selected_demo}...'):
            st.session_state['data'] = demo_datasets[selected_demo]
            st.session_state['data_source'] = 'demo'
            st.success(f"✅ {selected_demo} загружен! {len(demo_datasets[selected_demo])} записей.")
            st.rerun()


# ============================================================================
# DATA OVERVIEW SECTION
# ============================================================================

def data_overview_section(df: pd.DataFrame):
    """Display data overview with statistics."""
    st.markdown("### 📋 Обзор данных")
    
    if st.session_state.get('data_source') == 'demo':
        st.info("📊 Используются демо-данные. Вы можете загрузить свой файл для анализа реальных данных.")
    
    tab1, tab2, tab3 = st.tabs(["📊 Данные", "📈 Статистика", "ℹ️ Информация"])
    
    with tab1:
        st.dataframe(df, use_container_width=True, height=400)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Скачать данные (CSV)",
            data=csv,
            file_name="sales_data.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.markdown("#### Основные статистики")
        st.dataframe(df.describe(), use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Всего записей", f"{len(df):,}")
            st.metric("Столбцов", len(df.columns))
        with col2:
            st.metric("Пропущенных значений", df.isnull().sum().sum())
            st.metric("Размер памяти", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")


# ============================================================================
# KPI METRICS SECTION
# ============================================================================

def kpi_metrics_section(df: pd.DataFrame):
    """Display KPI metrics."""
    st.markdown("### 📊 Ключевые показатели")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if not numeric_cols:
        st.warning("В данных не найдено числовых столбцов для расчета метрик")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    revenue_col = None
    for col in numeric_cols:
        if any(keyword in col.lower() for keyword in ['revenue', 'sales', 'amount', 'сумма', 'выручка']):
            revenue_col = col
            break
    
    if revenue_col:
        total_revenue = df[revenue_col].sum()
        avg_revenue = df[revenue_col].mean()
        
        with col1:
            st.metric("Общая выручка", f"{total_revenue:,.2f}")
        with col2:
            st.metric("Средний чек", f"{avg_revenue:,.2f}")
    
    with col3:
        st.metric("Всего записей", f"{len(df):,}")
    
    with col4:
        st.metric("Всего столбцов", len(df.columns))


# ============================================================================
# VISUALIZATIONS SECTION
# ============================================================================

def visualizations_section(df: pd.DataFrame):
    """Interactive visualizations section."""
    st.markdown("### 📈 Визуализации")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not numeric_cols:
        st.warning("В данных не найдено числовых столбцов для визуализации")
        return
    
    chart_type = st.selectbox(
        "Выберите тип графика",
        ["Линейный график", "Столбчатая диаграмма", "Круговая диаграмма", 
         "Диаграмма рассеяния", "Box plot", "Гистограмма"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_col = st.selectbox("Ось X", categorical_cols + numeric_cols if categorical_cols else numeric_cols)
    with col2:
        y_col = st.selectbox("Ось Y (числовая)", numeric_cols)
    
    try:
        if chart_type == "Линейный график":
            fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} по {x_col}")
        elif chart_type == "Столбчатая диаграмма":
            if x_col in categorical_cols:
                df_grouped = df.groupby(x_col)[y_col].sum().reset_index()
                fig = px.bar(df_grouped, x=x_col, y=y_col, title=f"{y_col} по {x_col}")
            else:
                fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} по {x_col}")
        elif chart_type == "Круговая диаграмма":
            if x_col in categorical_cols:
                df_grouped = df.groupby(x_col)[y_col].sum().reset_index()
                fig = px.pie(df_grouped, names=x_col, values=y_col, title=f"Распределение {y_col}")
            else:
                st.warning("Для круговой диаграммы нужна категориальная переменная на оси X")
                return
        elif chart_type == "Диаграмма рассеяния":
            fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
        elif chart_type == "Box plot":
            if x_col in categorical_cols:
                fig = px.box(df, x=x_col, y=y_col, title=f"Распределение {y_col} по {x_col}")
            else:
                fig = px.box(df, y=y_col, title=f"Распределение {y_col}")
        elif chart_type == "Гистограмма":
            fig = px.histogram(df, x=y_col, title=f"Гистограмма {y_col}")
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Ошибка при создании графика: {str(e)}")


# ============================================================================
# ANALYSIS SECTION
# ============================================================================

def analysis_section(df: pd.DataFrame):
    """Advanced analysis section."""
    st.markdown("### 🔍 Анализ данных")
    
    analysis_type = st.selectbox(
        "Выберите тип анализа",
        ["Корреляционный анализ", "Топ-N записей", "Группировка данных"]
    )
    
    if analysis_type == "Корреляционный анализ":
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 2:
            st.warning("Для корреляционного анализа нужно минимум 2 числовых столбца")
            return
        
        st.markdown("#### Матрица корреляций")
        corr_matrix = df[numeric_cols].corr()
        fig = px.imshow(corr_matrix, labels=dict(color="Корреляция"),
                       x=corr_matrix.columns, y=corr_matrix.columns,
                       color_continuous_scale="RdBu", aspect="auto")
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Топ-N записей":
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("Сортировать по", numeric_cols)
        with col2:
            n = st.number_input("Количество записей", min_value=1, max_value=100, value=10)
        top_n = df.nlargest(n, sort_by)
        st.dataframe(top_n, use_container_width=True)
    
    elif analysis_type == "Группировка данных":
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not categorical_cols or not numeric_cols:
            st.warning("Нужны категориальные и числовые столбцы для группировки")
            return
        
        col1, col2, col3 = st.columns(3)
        with col1:
            group_by = st.selectbox("Группировать по", categorical_cols)
        with col2:
            agg_col = st.selectbox("Агрегировать столбец", numeric_cols)
        with col3:
            agg_func = st.selectbox("Функция", ["sum", "mean", "count", "min", "max"])
        
        grouped = df.groupby(group_by)[agg_col].agg(agg_func).reset_index()
        grouped.columns = [group_by, f"{agg_func}({agg_col})"]
        st.dataframe(grouped, use_container_width=True)
        fig = px.bar(grouped, x=group_by, y=f"{agg_func}({agg_col})")
        st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function."""
    init_session_state()
    
    with st.sidebar:
        st.title("📊 Навигация")
        
        if st.button("🔄 Загрузить новые данные", use_container_width=True):
            st.session_state['data'] = None
            st.session_state['data_source'] = None
            st.rerun()
        
        st.markdown("---")
        
        if st.session_state['data'] is not None:
            section = st.radio(
                "Выберите раздел",
                ["Обзор данных", "KPI и метрики", "Визуализации", "Анализ"],
                label_visibility="collapsed"
            )
            st.session_state['current_section'] = section
        
        st.markdown("---")
        st.markdown("### ℹ️ О приложении")
        st.info(
            "Sales Analytics Platform - инструмент для анализа данных о продажах. "
            "Загрузите свой файл или попробуйте демо-данные!"
        )
    
    if st.session_state['data'] is None:
        load_data_section()
    else:
        df = st.session_state['data']
        section = st.session_state.get('current_section', 'Обзор данных')
        
        if section == "Обзор данных":
            data_overview_section(df)
        elif section == "KPI и метрики":
            kpi_metrics_section(df)
        elif section == "Визуализации":
            visualizations_section(df)
        elif section == "Анализ":
            analysis_section(df)


if __name__ == "__main__":
    main()

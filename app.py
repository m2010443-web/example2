"""
Sales Analytics Platform - Main Application
Streamlit-based web application for sales data analysis and visualization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Dict, List
import io

# Import custom modules
from src import data_loader, analysis, plotting
import demo_data  # Демо-данные для Streamlit Cloud

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


def init_session_state():
    """Initialize session state variables."""
    if 'data' not in st.session_state:
        st.session_state['data'] = None
    if 'current_section' not in st.session_state:
        st.session_state['current_section'] = 'Загрузка данных'
    if 'data_source' not in st.session_state:
        st.session_state['data_source'] = None


def load_data_section():
    """Data loading section with demo data support."""
    st.title("📊 Sales Analytics Platform")
    st.markdown("### 📁 Загрузка данных")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Загрузите файл с данными о продажах",
        type=['csv', 'xlsx', 'xls'],
        help="Поддерживаются форматы: CSV, Excel (xlsx, xls)"
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner('Загрузка файла...'):
                # Determine file type
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
    
    # Demo data section
    st.markdown("---")
    st.markdown("### 🎬 Или попробуйте демо-данные")
    st.info("💡 Не хотите загружать файл? Попробуйте наши готовые датасеты!")
    
    # Get demo datasets
    demo_datasets = demo_data.get_demo_datasets()
    dataset_descriptions = demo_data.get_demo_description()
    
    # Create columns for selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_demo = st.selectbox(
            "Выберите демо-датасет:",
            [""] + list(demo_datasets.keys()),
            format_func=lambda x: "Выберите..." if x == "" else x
        )
    
    with col2:
        st.write("")  # Spacing
        load_demo = st.button(
            "📊 Загрузить демо",
            type="primary",
            disabled=not selected_demo,
            use_container_width=True
        )
    
    # Show description
    if selected_demo and selected_demo in dataset_descriptions:
        st.caption(f"ℹ️ {dataset_descriptions[selected_demo]}")
    
    # Load demo data
    if load_demo and selected_demo:
        with st.spinner(f'Загружаю {selected_demo}...'):
            st.session_state['data'] = demo_datasets[selected_demo]
            st.session_state['data_source'] = 'demo'
            st.success(f"✅ {selected_demo} загружен! {len(demo_datasets[selected_demo])} записей.")
            st.rerun()


def data_overview_section(df: pd.DataFrame):
    """Display data overview with statistics."""
    st.markdown("### 📋 Обзор данных")
    
    # Data source indicator
    if st.session_state.get('data_source') == 'demo':
        st.info("📊 Используются демо-данные. Вы можете загрузить свой файл для анализа реальных данных.")
    
    # Display tabs
    tab1, tab2, tab3 = st.tabs(["📊 Данные", "📈 Статистика", "ℹ️ Информация"])
    
    with tab1:
        st.dataframe(df, use_container_width=True, height=400)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Скачать данные (CSV)",
            data=csv,
            file_name="sales_data.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.markdown("####  Основные статистики")
        st.dataframe(df.describe(), use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Всего записей", f"{len(df):,}")
            st.metric("Столбцов", len(df.columns))
        with col2:
            st.metric("Пропущенных значений", df.isnull().sum().sum())
            st.metric("Размер памяти", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        st.markdown("#### Типы данных")
        dtypes_df = pd.DataFrame({
            'Столбец': df.columns,
            'Тип': df.dtypes.astype(str),
            'Пропуски': df.isnull().sum().values
        })
        st.dataframe(dtypes_df, use_container_width=True, hide_index=True)


def kpi_metrics_section(df: pd.DataFrame):
    """Display KPI metrics."""
    st.markdown("### 📊 Ключевые показатели")
    
    # Detect numeric and date columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if not numeric_cols:
        st.warning("В данных не найдено числовых столбцов для расчета метрик")
        return
    
    # Calculate metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Try to find revenue/sales column
    revenue_col = None
    for col in numeric_cols:
        if any(keyword in col.lower() for keyword in ['revenue', 'sales', 'amount', 'сумма', 'выручка']):
            revenue_col = col
            break
    
    if revenue_col:
        total_revenue = df[revenue_col].sum()
        avg_revenue = df[revenue_col].mean()
        
        with col1:
            st.metric(
                "Общая выручка",
                f"{total_revenue:,.2f}",
                help=f"Сумма всех значений в столбце {revenue_col}"
            )
        
        with col2:
            st.metric(
                "Средний чек",
                f"{avg_revenue:,.2f}",
                help=f"Среднее значение в столбце {revenue_col}"
            )
    
    with col3:
        st.metric(
            "Всего записей",
            f"{len(df):,}",
            help="Общее количество транзакций/записей"
        )
    
    with col4:
        # Try to calculate growth if date column exists
        date_cols = df.select_dtypes(include=['datetime64', 'object']).columns.tolist()
        if date_cols and revenue_col:
            try:
                df_temp = df.copy()
                df_temp[date_cols[0]] = pd.to_datetime(df_temp[date_cols[0]], errors='coerce')
                df_temp = df_temp.sort_values(date_cols[0])
                
                # Compare last vs previous period
                mid_point = len(df_temp) // 2
                recent_revenue = df_temp[revenue_col].iloc[mid_point:].sum()
                older_revenue = df_temp[revenue_col].iloc[:mid_point].sum()
                growth = ((recent_revenue - older_revenue) / older_revenue * 100) if older_revenue > 0 else 0
                
                st.metric(
                    "Рост",
                    f"{growth:.1f}%",
                    delta=f"{growth:.1f}%",
                    help="Сравнение второй половины данных с первой"
                )
            except:
                st.metric("Анализ роста", "N/A")
        else:
            st.metric("Всего столбцов", len(df.columns))


def visualizations_section(df: pd.DataFrame):
    """Interactive visualizations section."""
    st.markdown("### 📈 Визуализации")
    
    # Column selection
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not numeric_cols:
        st.warning("В данных не найдено числовых столбцов для визуализации")
        return
    
    # Chart type selection
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
    
    # Create visualization
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
        
        # Display chart
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Ошибка при создании графика: {str(e)}")


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
        
        fig = px.imshow(
            corr_matrix,
            labels=dict(color="Корреляция"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale="RdBu",
            aspect="auto"
        )
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
        
        # Visualization
        fig = px.bar(grouped, x=group_by, y=f"{agg_func}({agg_col})")
        st.plotly_chart(fig, use_container_width=True)


def main():
    """Main application function."""
    init_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        st.title("📊 Навигация")
        
        # Reset data button
        if st.button("🔄 Загрузить новые данные", use_container_width=True):
            st.session_state['data'] = None
            st.session_state['data_source'] = None
            st.rerun()
        
        st.markdown("---")
        
        # Section selection (only if data is loaded)
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
    
    # Main content
    if st.session_state['data'] is None:
        load_data_section()
    else:
        df = st.session_state['data']
        
        # Display selected section
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

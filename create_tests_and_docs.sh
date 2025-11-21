#!/bin/bash

# ==== tests/__init__.py ====
touch tests/__init__.py

# ==== tests/test_data_loader.py ====
cat > tests/test_data_loader.py << 'EOF'
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
EOF

# ==== tests/test_analysis.py ====
cat > tests/test_analysis.py << 'EOF'
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
EOF

# ==== tests/test_plotting.py ====
cat > tests/test_plotting.py << 'EOF'
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
EOF

# ==== README.md ====
cat > README.md << 'EOF'
# 📊 Sales Analytics Platform

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](#)

**👆 Попробуйте прямо сейчас - без установки! 👆**

Интерактивная платформа для анализа данных о продажах с встроенными демо-данными.

---

## ✨ Возможности

- 📁 **Загрузка данных** - поддержка CSV и Excel
- 🎬 **Демо-данные** - 3 готовых датасета для instant demo
- 📊 **Интерактивные дашборды** - KPI метрики и визуализации
- 📈 **Продвинутая аналитика** - корреляции, группировки, top-N
- 🎨 **Красивые графики** - Plotly для интерактивных визуализаций
- 💾 **Экспорт данных** - скачивание результатов в CSV

---

## 🚀 Три способа использования

| Способ | Описание | Время установки |
|--------|----------|----------------|
| 🌐 **Онлайн** | Кликните на badge выше | 0 минут |
| 🐳 **Docker** | `docker-compose up` | 2 минуты |
| 💻 **Из исходников** | `pip install -r requirements.txt` | 3 минуты |

---

## 📦 Быстрый старт (локально)

```bash
# Клонировать репозиторий
git clone https://github.com/YOUR_USERNAME/sales-analytics-platform.git
cd sales-analytics-platform

# Установить зависимости
pip install -r requirements.txt

# Запустить приложение
streamlit run app.py
```

Приложение откроется в браузере на `http://localhost:8501`

---

## 🐳 Docker

```bash
# Запустить с Docker Compose
docker-compose up

# Или собрать вручную
docker build -t sales-analytics .
docker run -p 8501:8501 sales-analytics
```

---

## 🎬 Демо-данные

Приложение включает 3 готовых датасета:

1. **📊 Детальные продажи** - 2000 записей с заказами, продуктами, регионами
2. **📅 Месячная статистика** - 12 месяцев агрегированных данных
3. **🏆 Топ продукты** - 10 самых популярных товаров

Просто выберите датасет и нажмите "Загрузить" - никаких файлов не нужно!

---

## 📊 Структура проекта

```
sales-analytics-platform/
├── app.py                 # Главное Streamlit приложение
├── demo_data.py           # Генератор демо-данных
├── requirements.txt       # Python зависимости
├── src/
│   ├── data_loader.py     # Загрузка и обработка данных
│   ├── analysis.py        # Аналитические функции
│   └── plotting.py        # Визуализации
├── tests/                 # Unit тесты
├── .streamlit/
│   └── config.toml        # Конфигурация Streamlit
└── README.md
```

---

## 🧪 Тестирование

```bash
# Запустить все тесты
pytest

# С покрытием
pytest --cov=src --cov-report=html
```

---

## 📚 Документация

- **Пользователь**: Встроенная помощь в приложении (кнопка "ℹ️")
- **Разработчик**: Docstrings в модулях + type hints

---

## 🤝 Contributing

Contributions welcome! Пожалуйста:

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

---

## 📞 Контакты

- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Email: your.email@example.com

---

<div align="center">

**Сделано с ❤️ и ☕**

[⬆ Вернуться наверх](#-sales-analytics-platform)

</div>
EOF

echo "Tests and docs created successfully!"

# Руководство по тестированию

## Обзор

Проект включает комплексную систему тестирования с автоматическим запуском через GitHub Actions.

## Структура тестов

```
tests/
├── __init__.py
├── test_data_loader.py    # Тесты загрузки и обработки данных
├── test_analysis.py        # Тесты анализа данных
└── test_plotting.py        # Тесты визуализации
```

## Покрытие тестами

### test_data_loader.py
- **TestDetectColumnTypes**: Определение типов колонок (numeric, categorical, datetime)
- **TestCleanData**: Очистка данных (удаление дубликатов, заполнение NaN)
- **TestLoadFunctions**: Загрузка CSV и Excel файлов

### test_analysis.py
- **TestCalculateBasicStats**: Базовая статистика (mean, median, std, quartiles)
- **TestCalculateCorrelation**: Корреляционный анализ
- **TestGroupAndAggregate**: Группировка и агрегация данных
- **TestDetectOutliers**: Обнаружение выбросов (IQR метод)

### test_plotting.py
- **TestCreateLineChart**: Линейные графики
- **TestCreateBarChart**: Столбчатые диаграммы
- **TestCreatePieChart**: Круговые диаграммы
- **TestCreateScatterPlot**: Диаграммы рассеяния
- **TestCreateCorrelationHeatmap**: Тепловые карты корреляции

## Запуск тестов локально

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск всех тестов

```bash
pytest
```

### Запуск с покрытием кода

```bash
pytest --cov=src --cov-report=html --cov-report=term
```

После выполнения откройте `htmlcov/index.html` для просмотра детального отчёта о покрытии.

### Запуск конкретного теста

```bash
# Запуск всех тестов в файле
pytest tests/test_data_loader.py

# Запуск конкретного класса тестов
pytest tests/test_analysis.py::TestCalculateBasicStats

# Запуск конкретного теста
pytest tests/test_analysis.py::TestCalculateBasicStats::test_basic_stats_simple_data
```

### Запуск с verbose режимом

```bash
pytest -v
```

## Проверка качества кода

### Линтинг с flake8

```bash
# Проверка всех файлов
flake8 .

# Проверка только критических ошибок
flake8 . --select=E9,F63,F7,F82
```

### Форматирование с black

```bash
# Проверка форматирования
black --check .

# Автоматическое форматирование
black .
```

### Сортировка импортов с isort

```bash
# Проверка сортировки
isort --check-only --diff .

# Автоматическая сортировка
isort .
```

### Проверка типов с mypy

```bash
mypy src --ignore-missing-imports
```

### Проверка безопасности

```bash
# Сканирование кода на уязвимости
bandit -r src/

# Проверка зависимостей
safety check
```

## GitHub Actions

### Автоматическое тестирование

При каждом push или pull request в ветки `main`, `master` или `develop` автоматически запускаются:

1. **Тесты на Python 3.9, 3.10, 3.11**
   - Установка зависимостей
   - Линтинг (flake8)
   - Проверка форматирования (black)
   - Проверка импортов (isort)
   - Проверка типов (mypy)
   - Запуск тестов с coverage

2. **Проверка безопасности**
   - Сканирование кода (bandit)
   - Проверка зависимостей (safety)

### Просмотр результатов

1. Перейдите в раздел **Actions** на GitHub
2. Выберите последний workflow run
3. Просмотрите результаты каждого job
4. Скачайте артефакты (отчёты о покрытии) при необходимости

### Статус тестов

Добавьте следующий badge в ваш README.md:

```markdown
![Tests](https://github.com/m2010443-web/example2/actions/workflows/tests.yml/badge.svg)
```

## Метрики покрытия

Цели проекта:
- **Общее покрытие**: > 80%
- **Критические модули**: > 90%

Текущее покрытие можно увидеть в отчётах GitHub Actions.

## Добавление новых тестов

### Шаблон теста

```python
"""Tests for new_module."""

import pytest
import pandas as pd
from src import new_module


class TestNewFunction:
    """Tests for new_function."""
    
    def test_basic_case(self):
        """Test basic functionality."""
        # Arrange
        input_data = ...
        expected = ...
        
        # Act
        result = new_module.new_function(input_data)
        
        # Assert
        assert result == expected
    
    def test_edge_case(self):
        """Test edge case."""
        # Test implementation
        pass
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            new_module.new_function(invalid_input)
```

### Best Practices

1. **Используйте классы** для группировки связанных тестов
2. **Описательные имена** для тестов (test_what_when_expected)
3. **Arrange-Act-Assert** паттерн
4. **Тестируйте граничные случаи** и обработку ошибок
5. **Изолированность** - каждый тест независим
6. **Быстрое выполнение** - избегайте длительных операций

## Отладка тестов

### Запуск с отладочной информацией

```bash
pytest -vv --tb=long
```

### Запуск с pdb (отладчик)

```bash
pytest --pdb
```

### Остановка на первой ошибке

```bash
pytest -x
```

## Continuous Integration

Все изменения должны:
1. ✅ Пройти все тесты
2. ✅ Соответствовать стандартам кодирования (flake8)
3. ✅ Иметь покрытие не менее 80%
4. ✅ Пройти проверки безопасности

## Полезные команды

```bash
# Запуск быстрых тестов (пропуск медленных)
pytest -m "not slow"

# Параллельный запуск тестов (требует pytest-xdist)
pytest -n auto

# Генерация XML отчёта для CI
pytest --junit-xml=report.xml

# Обновление snapshot тестов
pytest --snapshot-update
```

## Дополнительные ресурсы

- [pytest документация](https://docs.pytest.org/)
- [GitHub Actions документация](https://docs.github.com/en/actions)
- [Coverage.py документация](https://coverage.readthedocs.io/)
- [flake8 документация](https://flake8.pycqa.org/)

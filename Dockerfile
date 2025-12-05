# Используем официальный Python образ как базовый
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения в контейнер
COPY . .

# Открываем порт 8501 (стандартный порт Streamlit)
EXPOSE 8501

# Проверка здоровья контейнера
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Команда запуска приложения
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

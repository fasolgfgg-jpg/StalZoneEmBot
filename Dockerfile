# Используем легковесный образ Python
FROM python:3.11-slim

# Отключаем буферизацию (чтобы логи в консоли появлялись мгновенно)
# и создание .pyc файлов
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Europe/Moscow

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Сначала копируем только зависимости (для кэширования слоев)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в папку /app внутри контейнера
COPY . .

# Создаем папку под данные, если ее нет
RUN mkdir -p /app/data

# Запуск скрипта
CMD ["python", "Main.py"]
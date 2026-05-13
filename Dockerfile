FROM python:3.11.15

#WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода и модели
COPY ./app/ ./app/
COPY ./models/ ./models/
# Открьтие порта
EXPOSE 5000

# Запуск приложения

CMD ["python", "app/app.py"]

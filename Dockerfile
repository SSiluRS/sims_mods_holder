FROM python:3.11-slim

WORKDIR /app

# Отключаем буферизацию вывода, чтобы логи появлялись сразу
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Порт, определенный в app.py для production
EXPOSE 7066

CMD ["python", "app.py"]
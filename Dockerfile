# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_APP=server.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]

# Dockerfile (for a Flask app)
FROM python:3.10-slim

WORKDIR /app

# avoid bytecode and set env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use a production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]

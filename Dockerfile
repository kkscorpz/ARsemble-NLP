FROM python:3.10-slim  
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5005
CMD ["bash", "-c", "rasa run --enable-api --cors '*' --host 0.0.0.0 --port ${PORT:-5005}"]
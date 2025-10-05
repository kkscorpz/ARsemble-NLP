# ✅ Use Python 3.10.11 (stable & Rasa-compatible)
FROM python:3.10.11-slim

# Prevent Python from writing .pyc files & buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy only requirements first (for layer caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Then copy the rest of your app
COPY . .

# Expose the Rasa default port
EXPOSE 5005

# Train model (optional — comment out if model is already trained)
# RUN rasa train

# Start the Rasa server with API + CORS
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]

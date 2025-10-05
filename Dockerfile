# Use official Python 3.10 image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Rasa default)
EXPOSE 5005

# Run Rasa action server or bot
CMD ["rasa", "run", "--enable-api", "--cors", "*"]

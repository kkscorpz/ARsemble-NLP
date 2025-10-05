# Use Python 3.10 (Rasa-compatible)
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Rasa port
EXPOSE 5005

# Train model (optional if model not included)
RUN rasa train

# Start the Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
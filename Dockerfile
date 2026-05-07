# Use official Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (layer caching - faster rebuilds)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of project
COPY . .

# Expose both ports
EXPOSE 8000 8501

# Run both servers
CMD ["bash", "start.sh"]
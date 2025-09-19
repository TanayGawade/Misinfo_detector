# Use Python 3.11-slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["python", "-m", "streamlit", "run", "streamlitui.py", "--server.port=8501", "--server.address=0.0.0.0"]
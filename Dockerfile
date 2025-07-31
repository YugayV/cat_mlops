FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements/requirements.txt /app/requirements.txt

# Install Python dependencies including uvicorn explicitly
RUN pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir uvicorn[standard]

# Copy the correct model package with setup.py
COPY model_package/ /app/model_package/

# Install the model package
RUN cd /app/model_package && pip install -e .

# Copy API code
COPY api/ /app/api/

# Copy dataset to the expected location
# Copy dataset from correct location
# COPY Dataset.csv /app/model_package/catboost_model/datasets/Dataset.csv

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Updated CMD to properly handle PORT environment variable
CMD ["sh", "-c", "exec uvicorn api.app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1 --timeout-keep-alive 30 --access-log"]
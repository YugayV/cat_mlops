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
COPY requirements.txt /app/requirements.txt

# Install Python dependencies including uvicorn explicitly
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir uvicorn[standard]

# Copy the correct model package with setup.py
COPY catboost_mlops_project/cat_mlops/model_package/ /app/model_package/

# Copy API
COPY catboost_mlops_project/cat_mlops/api/ /app/api/
##
# Create directories for trained models and datasets
RUN mkdir -p /app/model_package/catboost_model/trained_models
RUN mkdir -p /app/model_package/catboost_model/datasets

# Copy dataset from correct location
COPY itern_2.1/dataset/Dataset.csv /app/model_package/catboost_model/datasets/Dataset.csv

# Install the model package as a Python package
RUN cd /app/model_package && pip install -e .

# Train model during build phase (not during startup)
RUN cd /app/model_package && python -m catboost_model.train_pipeline

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Use python -m uvicorn to ensure it's found in the Python path
CMD ["sh", "-c", "python -m uvicorn api.app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1 --timeout-keep-alive 30"]


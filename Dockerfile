FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY model_package/requirements/requirements.txt /app/requirements.txt
COPY api/requirements.txt /app/api_requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r api_requirements.txt

# Copy model package
COPY model_package/ /app/model_package/
RUN cd model_package && pip install -e .

# Copy API code
COPY api/ /app/api/

# Copy dataset
COPY dataset/ /app/model_package/catboost_model/datasets/

# Train model
RUN cd model_package && python -m catboost_model.train_pipeline

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
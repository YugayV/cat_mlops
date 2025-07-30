import os
import shutil

# Создание структуры директорий
directories = [
    "model_package/catboost_model",
    "model_package/catboost_model/config", 
    "model_package/catboost_model/datasets",
    "model_package/catboost_model/processing",
    "model_package/catboost_model/trained_models",
    "model_package/tests",
    "model_package/requirements",
    "api",
    "api/app",
    "api/tests", 
    ".circleci",
    "docker",
    "scripts",
    "docs"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

print("Project structure created successfully!")
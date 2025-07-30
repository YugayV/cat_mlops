#!/bin/bash

# Скрипт для локального тестирования

echo "=== Локальное тестирование CatBoost MLOps проекта ==="

# Создание виртуального окружения
echo "Создание виртуального окружения..."
python -m venv venv

# Активация виртуального окружения
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Установка зависимостей
echo "Установка зависимостей модели..."
pip install -r model_package/requirements/requirements.txt
pip install -r model_package/requirements/test_requirements.txt

echo "Установка зависимостей API..."
pip install -r api/requirements.txt

# Копирование датасета
echo "Копирование датасета..."
mkdir -p model_package/catboost_model/datasets
cp ../itern_2.1/dataset/Dataset.csv model_package/catboost_model/datasets/

# Установка пакета модели
echo "Установка пакета модели..."
cd model_package
pip install -e .

# Обучение модели
echo "Обучение модели..."
python -m catboost_model.train_pipeline

# Тестирование модели
echo "Тестирование модели..."
python -m pytest tests/ -v

cd ..

# Тестирование API
echo "Тестирование API..."
cd api
python -m pytest tests/ -v

echo "=== Локальное тестирование завершено ==="
echo "Для запуска API выполните: uvicorn api.app.main:app --reload"
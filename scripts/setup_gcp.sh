#!/bin/bash

# Скрипт для настройки Google Cloud Platform

echo "=== Настройка Google Cloud Platform ==="

# Проверка установки gcloud CLI
if ! command -v gcloud &> /dev/null; then
    echo "gcloud CLI не установлен. Установите его с https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Аутентификация
echo "Выполните аутентификацию в Google Cloud:"
gcloud auth login

# Создание проекта (опционально)
read -p "Введите ID проекта Google Cloud: " PROJECT_ID
gcloud config set project $PROJECT_ID

# Включение необходимых API
echo "Включение необходимых API..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Создание сервисного аккаунта для CircleCI
echo "Создание сервисного аккаунта для CircleCI..."
gcloud iam service-accounts create circleci-deployer \
    --display-name="CircleCI Deployer"

# Назначение ролей
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:circleci-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:circleci-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:circleci-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# Создание ключа для сервисного аккаунта
echo "Создание ключа для сервисного аккаунта..."
gcloud iam service-accounts keys create ~/gcp-key.json \
    --iam-account=circleci-deployer@$PROJECT_ID.iam.gserviceaccount.com

echo "=== Настройка завершена ==="
echo "Сохраните содержимое файла ~/gcp-key.json как переменную окружения GOOGLE_CLOUD_KEYS в CircleCI"
echo "Также установите переменную GOOGLE_PROJECT_ID = $PROJECT_ID в CircleCI"
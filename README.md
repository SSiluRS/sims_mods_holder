# Sims Mods Holder

[![Docker Image Version (Backend)](https://img.shields.io/docker/v/ssilurs/sims-mods-backend?label=Backend&logo=docker)](https://hub.docker.com/r/ssilurs/sims-mods-backend)
[![Docker Image Version (Frontend)](https://img.shields.io/docker/v/ssilurs/sims-mods-frontend?label=Frontend&logo=docker)](https://hub.docker.com/r/ssilurs/sims-mods-frontend)
[![CI/CD Build](https://github.com/SSiluRS/sims_mods_holder/actions/workflows/docker-build.yml/badge.badge.svg)](https://github.com/SSiluRS/sims_mods_holder/actions/workflows/docker-build.yml)

Веб-приложение для управления и каталогизации модов для The Sims. Позволяет добавлять ссылки на моды, автоматически парсить информацию (заголовок, картинка) и тегировать их.

## 🐳 Docker Images

Готовые образы доступны на Docker Hub:
- **Backend**: `ssilurs/sims-mods-backend`
- **Frontend**: `ssilurs/sims-mods-frontend`

```bash
docker pull ssilurs/sims-mods-backend:latest
docker pull ssilurs/sims-mods-frontend:latest
```

## 🛠 Технологический стек

- **Backend**: Python 3.11, Flask, SQLite / MySQL
- **Frontend**: Vue.js 3, Vite, Tailwind CSS
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions (Docker Hub push, GitHub Releases)

## 🚀 Быстрый старт (Docker)

Это рекомендуемый способ запуска приложения.

1. **Клонируйте репозиторий**
2. **Создайте файл .env** (необязательно для SQLite)
3. **Запустите через Docker Compose**:

```bash
docker-compose up -d
```

После запуска приложение будет доступно по адресам:
- **Frontend (UI)**: [http://localhost:8080](http://localhost:8080)
- **Backend (API)**: [http://localhost:7066](http://localhost:7066)

## 📦 CI/CD и Версионирование

В проекте настроен автоматический цикл сборки и публикации образов.

### Автоматическая сборка
- **Push в main/master**: Собирает образы с тегом `:main`.
- **Git Tags (v*)**: Собирает релизные образы с соответствующим тегом версии (например, `:1.1.4`) и обновляет `:latest`.

### Скрипт релиза
Для создания новой версии используйте PowerShell скрипт `release.ps1`:

```powershell
# Создаст тег v1.2.0, отправит его в репозиторий и запустит CI/CD
.\release.ps1 -Version 1.2.0
```
*Скрипт поддерживает многоуровневые версии, например `1.1.4.1`.*

## 💻 Ручной запуск (для разработки)

### Бэкенд
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r backend/requirements.txt
python backend/run.py
```

### Фронтенд
```bash
cd frontend
npm install
npm run dev
```

## 📁 Структура проекта

```
sims_mods_holder/
├── .github/workflows/  # CI/CD конфигурация
├── backend/            # Flask приложение
├── frontend/           # Vue.js приложение
├── release.ps1         # Скрипт для автоматизации релизов
├── docker-compose.yml  # Оркестрация контейнеров
└── ...
```

## ⚙️ Конфигурация

Основные переменные в `.env`:
- `APP_VERSION`: Версия приложения (отображается в футере).
- `DATABASE_TYPE`: `sqlite` (по умолчанию) или `mysql`.
- `FLASK_ENV`: `development` / `production`.
- `SECRET_KEY`: Секретный ключ приложения.


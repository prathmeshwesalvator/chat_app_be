FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /auth_service

# Install system deps + Redis
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    redis-server \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY auth_service/requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY auth_service/ .

EXPOSE 8000
EXPOSE 6379

# Start Redis + Django (Daphne)
CMD ["sh", "-c", "\
    redis-server --daemonize yes && \
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000 \
"]


# daphne -b 0.0.0.0 -p ${PORT:-8000} auth_service.asgi:application \




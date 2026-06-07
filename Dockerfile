FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Django dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Node / Tailwind
COPY package.json package-lock.json ./
RUN npm ci

# Project files 
COPY . .

# Build minified CSS (no env vars needed for this step)
RUN npm run minify

EXPOSE 8000

# Run migrate + collectstatic at startup so they see the real env vars
CMD sh -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p $PORT _core.asgi:application"
FROM python:3.12-slim

# Install system dependencies needed for psycopg2 (if postgres is used)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Run collectstatic (will collect white noise assets)
RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["gunicorn", "jobportal.wsgi.application", "--bind", "0.0.0.0:10000"]

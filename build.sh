#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing requirements..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Build complete!"

#!/bin/bash
# Migration script for Render deployment
# Run this manually in Render Shell after database is created

echo "Starting migrations..."

# Apply all migrations
python manage.py migrate --run-syncdb

# Create a superuser if needed (optional)
# python manage.py createsuperuser

echo "Migrations completed successfully!"
echo "You can now access the admin panel at /admin/"

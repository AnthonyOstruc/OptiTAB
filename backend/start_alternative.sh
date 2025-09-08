#!/bin/bash

# Alternative startup script for Render
echo "=== Alternative startup for OptiTAB ==="

# Navigate to backend directory
cd /opt/render/project/src/backend

# Set Python path and start gunicorn
export PYTHONPATH=/opt/render/project/src/backend
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 backendAPI.wsgi:application

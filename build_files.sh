#!/bin/bash
# Build script for Vercel deployment
set -e

echo "Building project..."
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear

echo "Build complete."


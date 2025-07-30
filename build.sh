#!/bin/bash
# Build script for Render deployment

echo "Starting build process..."

# Install Python dependencies
pip install -r requirements.txt

# Set environment variables for cloud deployment
export DATABASE_TYPE=postgresql

echo "Build completed successfully!" 
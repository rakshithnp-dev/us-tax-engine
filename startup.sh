#!/bin/bash

# Azure App Service startup script for Streamlit

echo "Starting US Tax Engine on Azure App Service..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start Streamlit with Azure-compatible settings
echo "Launching Streamlit application..."
streamlit run app.py \
    --server.port=8000 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --browser.gatherUsageStats=false

#!/bin/bash

echo ""
echo "========================================"
echo "PhishGuard - Phishing Detection Tool"
echo "========================================"
echo ""

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages if needed
echo "Checking dependencies..."
pip install -r requirements.txt -q

# Run the Flask application
echo ""
echo "========================================"
echo "Starting PhishGuard..."
echo "========================================"
echo ""
echo "The application is starting on:"
echo "  - Local: http://localhost:5000"
echo "  - Network: http://0.0.0.0:5000"
echo ""
echo "Press CTRL+C to stop the server."
echo ""

python app.py

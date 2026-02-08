#!/bin/bash
# AI Mock Interview System - Linux/Mac Startup Script

echo ""
echo "================================================"
echo "  AI MOCK INTERVIEW SYSTEM"
echo "================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo ""
    echo "Please create a .env file with your API key."
    echo "See .env.example for the format."
    echo ""
    exit 1
fi

echo "Starting the application..."
echo ""
echo "The web browser should open automatically."
echo "If not, manually open: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server when done."
echo ""
echo "================================================"
echo ""

# Start the Flask app
python3 app.py

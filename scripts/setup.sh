#!/bin/bash
# Setup script for Metaluminous Engine

set -e

echo "=== Metaluminous Engine Setup ==="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and configure your API keys and settings"
fi

# Start Docker services
echo ""
echo "Starting Docker services (PostgreSQL and Qdrant)..."
docker-compose up -d

# Wait for services to be ready
echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "Checking service health..."
docker-compose ps

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Install Ollama: https://ollama.ai"
echo "3. Pull models:"
echo "   ollama pull qwen2.5:72b-instruct-q4_K_M"
echo "   ollama pull deepseek-r1:70b"
echo "   ollama pull mixtral:8x22b"
echo "4. Run the server: python -m metaluminous.web.app"
echo ""

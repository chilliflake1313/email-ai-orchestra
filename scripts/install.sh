#!/bin/bash

set -e

echo "📧 Email AI Orchestra - Installation Script"
echo "==========================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

if ! command -v ollama &> /dev/null; then
    echo ""
    echo "⚠️  Ollama not found. Installing..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✓ Ollama found"
fi

echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

echo "✓ Virtual environment created"

echo ""
echo "📦 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Dependencies installed"

if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created - Please edit it with your credentials"
else
    echo "✓ .env file already exists"
fi

if [ ! -d logs ]; then
    echo ""
    echo "📁 Creating logs directory..."
    mkdir logs
fi

echo ""
echo "🤖 Pulling Ollama model..."
ollama pull mistral

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your email credentials"
echo "  2. Review config.json for rules"
echo "  3. Run: source venv/bin/activate"
echo "  4. Run: python scripts/check_env.py"
echo "  5. Run: python app.py --dry-run"
echo ""

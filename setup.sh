#!/bin/bash

# AI Agent Red-Teaming PoC Setup Script

echo "=================================="
echo "AI Agent Red-Teaming PoC Setup"
echo "=================================="

# Check Python version
echo ""
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

# Install core dependencies
echo ""
echo "Installing core dependencies..."
pip install -r requirements.txt

# Install scanners (optional, may fail if not available)
echo ""
echo "Installing red-teaming scanners..."
echo "Note: Some scanners may not be available yet."
pip install agentic-radar || echo "⚠️  agentic-radar not available"
pip install agentfence || echo "⚠️  agentfence not available"
pip install a2a-scanner || echo "⚠️  a2a-scanner not available"

# Create directories
echo ""
echo "Creating necessary directories..."
mkdir -p test_files
mkdir -p reports/agentic_radar
mkdir -p reports/agentfence
mkdir -p reports/a2a_scanner

# Check for .env file
echo ""
if [ ! -f .env ]; then
    echo "⚠️  .env file not found"
    echo "Please copy .env.example to .env and configure your credentials:"
    echo "  cp .env.example .env"
    echo "  nano .env  # or use your preferred editor"
else
    echo "✓ .env file found"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Configure your .env file (if not done already)"
echo "2. Test LLM connection: python llm_factory.py"
echo "3. Start API server: python api_server.py"
echo "4. Run all scans: python run_all_scans.py"
echo ""
echo "For more information, see README.md"

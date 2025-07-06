#!/bin/bash
# BEAT ADDICTS WordPress Setup Script

echo "🎵 BEAT ADDICTS WordPress Setup"
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1)
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv beat-addicts-env
source beat-addicts-env/bin/activate

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Set permissions
echo "Setting file permissions..."
chmod +x ../beat-addicts-core/*.py
chmod +x setup.sh

# Test installation
echo "Testing installation..."
cd ../beat-addicts-core/
python safe_wordpress_test.py

echo "✅ Setup complete!"
echo "📚 See installation-guide.md for next steps"

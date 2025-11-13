#!/bin/bash
# Setup script for Linux/Mac
# Run this script to set up the development environment

echo "Setting up AI-Powered Job Application Automation..."

# Check Python version
echo -e "\nChecking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"

# Create virtual environment
echo -e "\nCreating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo -e "\nActivating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo -e "\nUpgrading pip..."
pip install --upgrade pip

# Install requirements
echo -e "\nInstalling Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo -e "\nInstalling Playwright browsers..."
playwright install

echo -e "\nSetup complete!"
echo -e "\nNext steps:"
echo "1. Add your resume and documents to the data/ directory"
echo "2. Update config.yaml with your preferences"
echo "3. Update data/company_list.csv with target companies"
echo "4. Run: python scripts/embed_personal_docs.py"
echo "5. Run: python scripts/train_fit_model.py"


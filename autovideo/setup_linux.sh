#!/bin/bash

# AutoVideo Setup Script for Ubuntu (e.g., with NVIDIA 4090)
# Usage: ./setup_linux.sh

echo "========================================="
echo "   AutoVideo Setup (Ubuntu/Debian)       "
echo "========================================="

# 1. Update System & Install Dependencies
echo "[1/4] Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3-venv \
    python3-pip \
    ffmpeg \
    sox \
    libsox-fmt-all \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-science \
    fonts-noto-cjk \
    fonts-noto-color-emoji

# 2. Python Virtual Environment
echo "[2/4] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo " -> venv created."
else
    echo " -> venv already exists."
fi

# Activate venv for the script execution context
source venv/bin/activate

# 3. Python Dependencies
echo "[3/4] Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Manually ensure torch is installed correctly if needed (optional)
# pip install torch torchvision torchaudio

# 4. Final Check
echo "[4/4] Verifying installation..."
python -c "import manim; print('Manim version:', manim.__version__)"
python -c "import moviepy; print('MoviePy version:', moviepy.__version__)"

echo "========================================="
echo "   Setup Complete!                       "
echo "========================================="
echo "To activate the environment manually, run:"
echo "    source venv/bin/activate"
echo ""
echo "To run a test generation:"
echo "    python pipeline.py build --project projects/number1 --skip-rvc"

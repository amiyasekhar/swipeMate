#!/bin/bash
sudo apt-get update
sudo apt-get install -y clang libopenblas-dev liblapack-dev libjxl-dev
sudo apt-get update && sudo apt-get install -y \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libjpeg-dev \
    libpng-dev
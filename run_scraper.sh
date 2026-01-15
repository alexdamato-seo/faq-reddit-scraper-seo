#!/bin/bash
# Simple one-click script to run the Reddit scraper
# Just double-click this file!

echo "=========================================="
echo "Reddit Microscopy FAQ Scraper"
echo "=========================================="
echo ""
echo "Installing dependencies..."
pip install requests pandas --quiet

echo ""
echo "Starting scraper..."
echo "This will take 30-60 minutes."
echo "You can minimize this window and come back later."
echo ""

python3 reddit_scraper_no_api.py

echo ""
echo "=========================================="
echo "DONE! Check the 'output' folder for your results."
echo "Press any key to close..."
read -n 1

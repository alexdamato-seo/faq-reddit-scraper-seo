# Beginner's Guide - No Terminal Experience Needed!

This guide will help you run the scraper with **zero terminal experience**. Just follow these simple steps.

---

## Step 1: Check if You Have Python

### Windows:
1. Press the **Windows key** on your keyboard
2. Type "cmd" and press Enter (a black window will open)
3. Type `python --version` and press Enter
4. If you see something like "Python 3.11.0" - you're good! Skip to Step 2.
5. If you see an error, download Python from: https://www.python.org/downloads/
   - Click the big yellow "Download Python" button
   - Run the installer
   - ✅ **IMPORTANT**: Check the box that says "Add Python to PATH" during installation
   - Click "Install Now"

### Mac:
1. Press **Command + Space** on your keyboard
2. Type "terminal" and press Enter
3. Type `python3 --version` and press Enter
4. If you see "Python 3.x.x" - you're good! Skip to Step 2.
5. If not, install from: https://www.python.org/downloads/

---

## Step 2: Download the Scraper

### Option A: Download ZIP (Easiest)
1. Go to your GitHub repository page
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Find the ZIP file in your Downloads folder
5. Right-click it and choose "Extract All" (Windows) or double-click it (Mac)
6. Move the extracted folder to your Desktop (or anywhere you want)

### Option B: If you have Git installed
1. Press Windows key (or Command+Space on Mac)
2. Type "cmd" (Windows) or "terminal" (Mac) and press Enter
3. Copy and paste this:
```
cd Desktop
git clone https://github.com/alexdamato-seo/faq-reddit-scraper-seo.git
```
4. Press Enter

---

## Step 3: Run the Scraper (Super Easy!)

### Windows:
1. Open the `faq-reddit-scraper-seo` folder
2. Find the file called **`run_scraper.bat`**
3. **Double-click it**
4. A window will open and start running
5. Wait 30-60 minutes (you can minimize the window)
6. When done, look in the `output` folder for your results!

### Mac/Linux:
1. Open the `faq-reddit-scraper-seo` folder
2. Right-click on **`run_scraper.sh`**
3. Choose "Open With" → "Terminal" (or just double-click)
4. If it says "permission denied":
   - Open Terminal (Command + Space, type "terminal")
   - Type: `cd ` (with a space after cd)
   - Drag the `faq-reddit-scraper-seo` folder into the terminal window
   - Press Enter
   - Type: `chmod +x run_scraper.sh`
   - Press Enter
   - Type: `./run_scraper.sh`
   - Press Enter
5. Wait 30-60 minutes
6. When done, look in the `output` folder for your results!

---

## Step 4: View Your Results

After the scraper finishes, you'll have these files in the `output` folder:

### 📊 microscopy_faqs.csv
- **How to open**: Double-click to open in Excel or Google Sheets
- **What it contains**: All the questions in a spreadsheet
- **What to do with it**: Sort, filter, analyze the data

### 📄 microscopy_faqs.json
- **How to open**: Open with a text editor (Notepad, TextEdit, VS Code)
- **What it contains**: All the questions in structured format
- **What to do with it**: Use for programming or import into other tools

### 📁 microscopy_faqs_by_category.json
- **How to open**: Open with a text editor
- **What it contains**: Questions organized by equipment category
- **What to do with it**: Perfect for creating category-specific FAQ pages

---

## What You'll See While It Runs

The window will show text like this:

```
==========================================
Reddit Microscopy FAQ Scraper
==========================================

Installing dependencies...
Done!

Starting scraper...
This will take 30-60 minutes.
You can minimize this window and come back later.

Searching for: Inverted Microscopes
  Searching r/microscopy for 'inverted microscope'
    Found: Best inverted microscope for cell culture?... (score: 25)
  Searching r/labrats for 'inverted microscope'
    Found: Olympus vs Nikon inverted scope?... (score: 18)
...
```

**Don't worry!** This is normal. The scraper is working through all the categories.

---

## Troubleshooting

### "python is not recognized" (Windows)
- You need to install Python (see Step 1)
- Make sure you checked "Add Python to PATH" during installation

### "Permission denied" (Mac/Linux)
- Open Terminal
- Navigate to the folder (drag folder into Terminal after typing `cd `)
- Type: `chmod +x run_scraper.sh`
- Try running again

### "Module not found" error
- The dependencies didn't install correctly
- Open cmd (Windows) or Terminal (Mac)
- Type: `pip install requests pandas`
- Press Enter
- Try running the scraper again

### Nothing happens when I double-click
- Right-click the file instead
- Choose "Open" or "Run"
- On Mac, you might need to go to System Preferences → Security & Privacy and allow the app

---

## How Long Will It Take?

- **Search time**: 30-60 minutes (searches 19 subreddits × 7 categories)
- **Why so long?**: We wait 2 seconds between each request to be respectful to Reddit
- **Can I stop it?**: Yes! Just close the window. You can run it again later.
- **Can I use my computer?**: Yes! Minimize the window and do other things.

---

## What You'll Get

**Expected results:**
- 200-350 real microscopy questions from Reddit
- Questions about: inverted, confocal, digital, upright, stereo microscopes, digital pathology, and microscope cameras
- Data includes: question text, upvotes, comments, URLs, timestamps
- Ready to use for SEO content creation!

---

## Still Need Help?

If you're stuck, try these:

1. **Take a screenshot** of any error message
2. **Copy the error text** from the window
3. Send it to your technical team or post in the GitHub issues

Or just email the whole `faq-reddit-scraper-seo` folder to someone technical - they'll know what to do!

---

## What's Next?

Once you have the data:
1. Open `microscopy_faqs.csv` in Excel
2. Sort by "score" (upvotes) to find the most popular questions
3. Filter by "category" to see questions for each microscope type
4. Use these questions to create FAQ content for your website
5. Address pain points and comparisons that customers care about

**Pro tip**: The `sample_output` folder has examples of what your results will look like!

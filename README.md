# Movie Scraper

This project uses **Selenium** to scrape movie details from the **IMDb Top Chart**, including the **movie title**, **year**, and **directors**. It is designed to run daily via a **Bash script** with a scheduler.

## Project Features

- **Scrape Movie Information**: Extracts movie title, release year, and director names from the IMDb Top 250 list.
- **Track Ranking Changes**: Compares the current day's rankings with the previous day's data to track up, down, or no change in the rankings.
- **CSV Output**: Saves the scraped data into a CSV file, with historical tracking of ranking changes.
- **Daily Execution**: Automates the scraping process to run daily via a Bash script with a scheduler (e.g., cron job).

## Requirements

1. **Selenium**: A web automation tool used to scrape the IMDb page.
2. **Python 3.x**: For writing and running the script.
3. **WebDriver**: A browser automation driver (e.g., ChromeDriver for Chrome or GeckoDriver for Firefox).
4. **CSV**: To store the scraped data.

### Installation

1. Install the required Python libraries:

   ```bash
   pip install selenium
   pip install pandas
   ```

   or

   ```bash
   pip install -r requirements.txt
   ```

2. Install the appropriate WebDriver:

   - [Download ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
   - [Download GeckoDriver](https://github.com/mozilla/geckodriver/releases)

3. Make sure the WebDriver executable is in your system's `PATH` or specify its location in the script.

## Script Overview

### 1. Scraping the Movie Data

The script scrapes the IMDb Top 250 list to gather the following details for each movie:

- **Movie Title**
- **Release Year**
- **Director(s)**

### 2. Tracking Ranking Changes

If there is previous day data available, the script compares the rankings of movies to track:

- **Up**: Movie rank has improved.
- **Down**: Movie rank has dropped.
- **No Change**: Movie rank remains the same.

### 3. Saving the Data

- The data is stored in a **CSV file**.
- Each row in the CSV contains the following fields:
  - **Rank**
  - **Movie Title**
  - **Release Year**
  - **Directors**
  - **Ranking Change** (if applicable)

### 4. Bash Script

To run the script daily, create a bash script (`run_scraper.sh`) and set it up with a scheduler like `cron`.

Example `run_scraper.sh`:

```bash
#!/bin/bash

# Navigate to the project directory
cd /path/to/your/project

# Run the Python script
python3 movie_scraper.py
```

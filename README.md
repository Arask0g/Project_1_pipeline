# Weather Data Pipeline

A Python data pipeline that fetches real-time weather data for multiple cities, 
analyzes it, stores it in PostgreSQL, and exports a CSV report.

## What it does
- Fetches live weather data from wttr.in API for multiple cities
- Parses and structures the data using pandas
- Performs statistical analysis with numpy
- Stores all readings in a PostgreSQL database with automatic timestamps
- Exports a CSV report

## Tech used
- Python, requests, pandas, numpy, psycopg2, PostgreSQL

## How to run
1. Create and activate a virtual environment
2. Run `pip install -r requirements.txt`
3. Create a PostgreSQL database called `weather_db`
4. Run `python pipeline.py`
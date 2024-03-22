# Flight Price Tracker

## Overview
This project is a Python script that uses Selenium to track flight prices from Krakow to Istanbul. It can be configured to run periodically on your local machine or on a cloud platform like AWS to automatically fetch the latest prices every few hours.

## Features
- Scrapes flight prices from a specified website
- Customizable search parameters (departure city, destination city, dates, etc.)
- Can be configured to run on a schedule using cron jobs (local) or AWS Lambda (cloud)
- Saves price data for analysis or visualization

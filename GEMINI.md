# GEMINI.md

## Project Overview

This project enables GEMINI to autonomously analyze Strava fitness data and generate periodic reports that quantify and visualize training progression. The focus is on measuring improvements in physiological efficiency, discipline, and consistency using available Strava data.

The agent has successfully authenticated with the Strava API, fetched activity and stream data, and calculated a variety of performance metrics. The final output is a PDF report that visualizes these metrics.

## Project Goals

GEMINI has successfully:

- Authenticated with the Strava API and handled token refresh.
- Extracted and persisted activity and stream-level data to CSV files.
- Computed a set of performance metrics, including:
    - Pace vs. Heart Rate Efficiency
    - Cardiac Drift
    - Heart Rate Stability (Standard Deviation)
    - Time in Heart Rate Zones
    - Zone Transitions
- Visualized and summarized these metrics in a structured PDF report.

## Key Metrics

The agent is currently calculating and visualizing the following metrics:

- **Pace vs. Heart Rate Efficiency:** Tracking speed per heart rate beat over time.
- **Cardiac Drift:** Measuring the change in efficiency over the course of a run.
- **Heart Rate Stability:** Quantifying the variability of heart rate during activities.
- **Zone Discipline:** Calculating the percentage of time spent in each of the five heart rate zones.
- **Zone Transitions:** Counting the number of times the user moves between heart rate zones.

## Technical Stack

- Python 3.x
- Virtual environment: `venv`
- Key Libraries:
    - `stravalib` for Strava API interaction
    - `pandas` for data manipulation
    - `matplotlib` for plotting
    - `fpdf` for PDF generation
    - `python-dotenv` for environment variable management

## Strava Integration

- The agent uses a `.env` file to store Strava API credentials (client ID, client secret, and refresh token).
- The `src/authenticate.py` script handles the OAuth2 authentication flow.

## Data Storage

- Raw activity data is stored in `data/activities.csv`.
- Detailed stream data is stored in `data/streams.csv`.
- Calculated metrics are stored in `data/metrics.csv`.

## Reporting

- The `src/generate_report.py` script creates a PDF report named `report.pdf` in the `reports` directory.
- The report includes time-series plots for key metrics and a heart rate zone distribution chart.
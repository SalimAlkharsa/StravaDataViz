# GEMINI.md

## Project Overview

This project enables GEMINI to autonomously analyze Strava fitness data and generate periodic reports that quantify and visualize training progression. The focus is on measuring improvements in physiological efficiency, discipline, and consistency using available Strava data.

The agent has successfully authenticated with the Strava API, fetched activity and stream data, calculated a variety of performance metrics, and generates a comprehensive PDF report segmented by activity type.

## Project Goals

GEMINI has successfully:

- Authenticated with the Strava API and handled token refresh.
- Extracted and persisted activity and stream-level data to CSV files.
- Computed a set of performance metrics, including:
    - Pace vs. Heart Rate Efficiency (overall and split-based)
    - Cardiac Drift
    - Heart Rate Stability (Standard Deviation)
    - Time spent in each Heart Rate Zone (absolute and percentage)
    - Zone Transitions
    - Weekly Time in Zone 2
- Visualized and summarized these metrics in a structured PDF report, segmented by activity type (Run, Ride, then others alphabetically).
- Implemented a modular `main.py` script for flexible pipeline execution.

## Key Metrics

The agent is currently calculating and visualizing the following metrics:

- **Pace vs. Heart Rate Efficiency:** Tracking speed per heart rate beat over time, with comparisons between the first and second halves of an activity.
- **Cardiac Drift:** Measuring the change in efficiency (HR/Pace ratio) over the course of a run.
- **Heart Rate Stability:** Quantifying the variability (standard deviation) of heart rate during activities, for both halves of an activity.
- **Time in Heart Rate Zones:** Calculating the absolute time and percentage of time spent in each of the five heart rate zones based on age-predicted maximum heart rate.
- **Zone Transitions:** Counting the number of times the user moves between heart rate zones within an activity.
- **Weekly Time in Zone 2:** Aggregating and visualizing the total time spent in Heart Rate Zone 2 on a weekly basis.

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
- The report is segmented by activity type, with each type having its own section containing 5 plots.
- Activity types are ordered as 'Run', 'Ride', then others alphabetically.

## Usage

The project can be run using the `main.py` script with command-line arguments to control which steps of the pipeline are executed. This allows for flexible and efficient operation.

Example:
```bash
python main.py --fetch --calculate --report
```

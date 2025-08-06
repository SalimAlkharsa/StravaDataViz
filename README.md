# Strava Performance Analytics

This project analyzes your Strava data to provide insights into your fitness progression. It automatically fetches your activity and stream data, calculates key performance metrics, and generates a PDF report with visualizations.

## Features

- **Strava Integration:** Securely connects to the Strava API to fetch your data.
- **Performance Metrics:** Calculates a variety of metrics, including:
    - Pace vs. Heart Rate Efficiency
    - Cardiac Drift
    - Heart Rate Stability (Standard Deviation)
    - Time in Heart Rate Zones
    - Zone Transitions
- **PDF Reporting:** Generates a comprehensive PDF report with plots and summaries of your key metrics.

## How to Use

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set Up Credentials:**
    - Create a file named `.env` in the root of the project.
    - Add your Strava API credentials to the `.env` file:
        ```
        STRAVA_CLIENT_ID=your_client_id
        STRAVA_CLIENT_SECRET=your_client_secret
        ```

3.  **Authenticate with Strava:**
    - Run the authentication script:
        ```bash
        python src/authenticate.py
        ```
    - Follow the on-screen instructions to authorize the application.

4.  **Fetch Data:**
    - Fetch your activities:
        ```bash
        python src/fetch_activities.py
        ```
    - Fetch your activity streams:
        ```bash
        python src/fetch_streams.py
        ```

5.  **Calculate Metrics:**
    ```bash
    python src/calculate_metrics.py
    ```

6.  **Generate Report:**
    ```bash
    python src/generate_report.py
    ```
    The report will be saved to `reports/report.pdf`.

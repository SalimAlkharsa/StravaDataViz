# Strava Performance Analytics

This project analyzes your Strava data to provide insights into your fitness progression. It automatically fetches your activity and stream data, calculates key performance metrics, and generates a PDF report with visualizations.

## Features

- **Strava Integration:** Securely connects to the Strava API to fetch your data.
- **Performance Metrics:** Calculates a variety of metrics, including:
    - Pace vs. Heart Rate Efficiency (overall and split-based)
    - Cardiac Drift
    - Heart Rate Stability (Standard Deviation)
    - Time spent in each Heart Rate Zone (absolute and percentage)
    - Zone Transitions
    - Weekly Time in Zone 2
- **PDF Reporting:** Generates a comprehensive PDF report with 5 plots per activity type, segmented and ordered (Run, Ride, then others alphabetically).

## How to Use

The project can be run using the `main.py` script with command-line arguments to control the execution flow.

1.  **Install Dependencies:**
    First, ensure your virtual environment is activated, then install the required libraries:
    ```bash
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Set Up Credentials:**
    - Create a file named `.env` in the root of the project.
    - Add your Strava API credentials to the `.env` file. You will need your `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET`.
        ```
        STRAVA_CLIENT_ID=your_client_id
        STRAVA_CLIENT_SECRET=your_client_secret
        ```

3.  **Run the Pipeline:**
    Use the `main.py` script with the desired arguments. You can combine arguments as needed.

    - **To run the entire pipeline (authentication, fetch, calculate, report):**
        ```bash
        python main.py --all
        ```

    - **To run only specific steps:**
        - **Authenticate with Strava:** (Required for first-time setup or if tokens expire)
            ```bash
            python main.py --authenticate
            ```
            Follow the on-screen instructions to authorize the application in your browser.

        - **Fetch Data:** (Fetches activities and detailed streams)
            ```bash
            python main.py --fetch
            ```

        - **Calculate Metrics:** (Processes raw data into performance metrics)
            ```bash
            python main.py --calculate
            ```

        - **Generate Report:** (Creates the PDF report in `reports/report.pdf`)
            ```bash
            python main.py --report
            ```

    - **Get help on arguments:**
        ```bash
        python main.py --help
        ```

## Project Structure

- `main.py`: Main entry point for the pipeline.
- `src/authenticate.py`: Handles Strava API authentication.
- `src/fetch_activities.py`: Fetches high-level activity data.
- `src/fetch_streams.py`: Fetches detailed stream data for activities.
- `src/calculate_metrics.py`: Calculates performance metrics from raw data.
- `src/generate_report.py`: Generates the segmented PDF report.
- `data/`: Stores raw and processed CSV data.
- `reports/`: Stores generated PDF reports and temporary plot images.
- `.env`: Stores sensitive API credentials (ignored by Git).
- `requirements.txt`: Lists Python dependencies.
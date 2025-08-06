import argparse
from src.authenticate import authenticate
from src.fetch_activities import fetch_activities
from src.fetch_streams import fetch_streams
from src.calculate_metrics import calculate_metrics
from src.generate_report import generate_report

def main():
    """
    Runs the Strava data analysis pipeline with command-line arguments to control each step.
    """
    parser = argparse.ArgumentParser(description="Strava Data Analysis Pipeline")
    parser.add_argument('--authenticate', action='store_true', help='Run the authentication process.')
    parser.add_argument('--fetch', action='store_true', help='Fetch activities and streams from Strava.')
    parser.add_argument('--calculate', action='store_true', help='Calculate metrics from the raw data.')
    parser.add_argument('--report', action='store_true', help='Generate the PDF report.')
    parser.add_argument('--all', action='store_true', help='Run the entire pipeline.')

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    if args.all or args.authenticate:
        print("\n--- Running Step: Authenticating with Strava ---")
        authenticate()

    if args.all or args.fetch:
        print("\n--- Running Step: Fetching Activities ---")
        fetch_activities()
        print("\n--- Running Step: Fetching Activity Streams ---")
        fetch_streams()

    if args.all or args.calculate:
        print("\n--- Running Step: Calculating Performance Metrics ---")
        calculate_metrics()

    if args.all or args.report:
        print("\n--- Running Step: Generating PDF Report ---")
        generate_report()

    print("\nPipeline steps finished.")

if __name__ == '__main__':
    main()
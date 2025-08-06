
import os
import pandas as pd
from dotenv import load_dotenv
from stravalib.client import Client

def fetch_activities():
    """
    Fetches all activities from the Strava API and saves them to a CSV file.
    """
    load_dotenv()

    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

    client = Client()

    # Refresh the token
    token_response = client.refresh_access_token(client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)
    client.access_token = token_response['access_token']

    activities = client.get_activities()

    data = []
    for activity in activities:
        data.append({
            'id': activity.id,
            'name': activity.name,
            'distance': activity.distance,
            'moving_time': activity.moving_time,
            'elapsed_time': activity.elapsed_time,
            'total_elevation_gain': activity.total_elevation_gain,
            'type': activity.type,
            'start_date': activity.start_date,
            'average_speed': activity.average_speed,
            'average_heartrate': activity.average_heartrate,
            'max_heartrate': activity.max_heartrate,
        })

    df = pd.DataFrame(data)
    df.to_csv('data/activities.csv', index=False)

    print("Successfully fetched and saved activities to data/activities.csv")

if __name__ == '__main__':
    fetch_activities()

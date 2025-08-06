
import os
import pandas as pd
from dotenv import load_dotenv
from stravalib.client import Client

def fetch_streams():
    """
    Fetches the stream data for each activity in the activities.csv file.
    """
    load_dotenv()

    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

    client = Client()

    # Refresh the token
    token_response = client.refresh_access_token(client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)
    client.access_token = token_response['access_token']

    activities_df = pd.read_csv('data/activities.csv')

    all_streams_data = []

    for index, row in activities_df.iterrows():
        activity_id = row['id']
        print(f"Fetching streams for activity {activity_id}")
        try:
            streams = client.get_activity_streams(activity_id, types=['time', 'latlng', 'distance', 'altitude', 'velocity_smooth', 'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth'])
            
            if streams:
                # Convert streams to a dictionary
                stream_data = {stream_type: stream.data for stream_type, stream in streams.items()}
                # Get the length of the first stream to create a dataframe
                stream_length = len(next(iter(stream_data.values())))
                # Create a dataframe for the current activity
                activity_streams_df = pd.DataFrame(stream_data)
                print(f"Columns for activity {activity_id}: {activity_streams_df.columns.tolist()}")
                activity_streams_df['activity_id'] = activity_id
                all_streams_data.append(activity_streams_df)

        except Exception as e:
            print(f"Error fetching streams for activity {activity_id}: {e}")

    if all_streams_data:
        # Concatenate all dataframes
        final_df = pd.concat(all_streams_data, ignore_index=True)
        final_df.to_csv('data/streams.csv', index=False)
        print("Successfully fetched and saved all stream data to data/streams.csv")
    else:
        print("No stream data found for any of the activities.")

if __name__ == '__main__':
    fetch_streams()

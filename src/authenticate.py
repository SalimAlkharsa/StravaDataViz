import os
from dotenv import load_dotenv
from stravalib.client import Client

def authenticate():
    """
    Authenticates with the Strava API using credentials from the .env file.
    """
    load_dotenv()

    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")

    client = Client()

    # Always run the authentication flow
    authorize_url = client.authorization_url(client_id=client_id, redirect_uri='http://localhost/exchange_token', scope=['read_all','profile:read_all','activity:read_all'], approval_prompt='force')
    print(f"Click here to authorize: {authorize_url}")

    authorization_code = input("Enter the authorization code from the redirect URL: ")

    token_response = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=authorization_code)

    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']

    with open('.env', 'w') as f:
        f.write(f"STRAVA_CLIENT_ID={client_id}\n")
        f.write(f"STRAVA_CLIENT_SECRET={client_secret}\n")
        f.write(f"STRAVA_REFRESH_TOKEN={refresh_token}\n")
        f.write(f"STRAVA_ACCESS_TOKEN={access_token}\n")

    print("Authentication successful! Refresh and access tokens saved to .env file.")

    return client

if __name__ == '__main__':
    authenticate()
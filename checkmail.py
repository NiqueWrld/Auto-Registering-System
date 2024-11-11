import requests

# Set your app registration details
tenant_id = 'YOUR_TENANT_ID'  # The tenant ID you registered
client_id = 'YOUR_CLIENT_ID'  # The client ID you registered
client_secret = 'YOUR_CLIENT_SECRET'  # The client secret for authentication

# API URLs
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
graph_api_url = 'https://graph.microsoft.com/v1.0/users'

# Get the access token using client credentials
def get_access_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }

    response = requests.post(token_url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print('Error fetching access token:', response.text)
        return None

# Fetch user details by email
def get_user_details_by_email(email):
    access_token = get_access_token()

    if access_token:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # API endpoint to get user details by email
        response = requests.get(f'{graph_api_url}/{email}', headers=headers)
        
        if response.status_code == 200:
            return response.json()  # Return user details in JSON format
        else:
            return f"Error: {response.status_code} - {response.text}"
    else:
        return "Unable to authenticate. Please check your credentials."

# Example usage
email = '22370908@dut4life.ac.za'  # Replace with the actual email address
user_details = get_user_details_by_email(email)
print(user_details)

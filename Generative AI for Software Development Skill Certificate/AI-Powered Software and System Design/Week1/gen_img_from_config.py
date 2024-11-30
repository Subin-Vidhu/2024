import requests
import json

# Load the configuration from the external file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Extract the API key and URL from the config
api_key = config['api_key']
url = config['url']

# Update headers with the authorization token
headers = config['headers']
headers['Authorization'] = f"Bearer {api_key}"

# Extract the payload from the config
payload = config['payload']

# Send a POST request to the OpenAI API
response = requests.post(url, headers=headers, 
 data=json.dumps(payload))

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()

    # Extract the URL of the generated image
    image_url = data['data'][0]['url']

    print(f"Image URL: {image_url}")
else:
    print(f"Failed to generate image: {response.status_code}")
    print(response.text)
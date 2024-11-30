# Define your OpenAI API key
api_key = "your_openai_api_key"

# Define the endpoint URL
url = "https://api.openai.com/v1/images/generations"

# Set up the headers, including authorization with your API key
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Define the payload with your desired prompt and other parameters
payload = {
    "prompt": "A futuristic cityscape at dusk with flying cars and neon lights",
    "n": 1,  # Number of images to generate
    "size": "1024x1024"  # Size of the generated image
}

# Send a POST request to the OpenAI API
response = requests.post(url, headers=headers, data=json.dumps(payload))

"""Decoding the response
The format of the output response from the Chat Completions endpoint is an object where the message can be accessed by selecting the appropriate fields.

In this example, you've just submitted a request to the API to list three Python libraries with the year they were first released, and it has returned a response."""
"""
Formatting model response as JSON
As a librarian cataloging new books, you aim to leverage the OpenAI API to automate the creation of a JSON file from text notes you received from a colleague. Your task is to extract relevant information such as book titles and authors and to do this, you use the OpenAI API to convert the text notes, that include book titles and authors, into structured JSON files."""

# Create the OpenAI client
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create the request
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
   {"role": "user", "content": "I have these notes with book titles and authors: New releases this week! The Beholders by Hester Musson, The Mystery Guest by Nita Prose. Please organize the titles and authors in a json file."}
  ],
  # Specify the response format
  response_format={"type": "json_object"}
)

# Print the response
print(response.choices[0].message.content)

"""Handling exceptions
You are working at a logistics company on developing an application that uses the OpenAI API to check the shipping address of your top three customers. The application will be used internally and you want to make sure that other teams are presented with an easy to read message in case of error.

To address this requirement, you decide to print a custom message in case the users fail to provide a valid key for authentication, and use a try and except block to handle that."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Use the try statement
try: 
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[message]
    )
    # Print the response
    print(response.choices[0].message.content)
# Use the except statement
except openai.AuthenticationError as e:
    print("Please double check your authentication key and try again, the one provided is not valid.")

"""Avoiding rate limits with retry
You've created a function to run Chat Completions with a custom message but have noticed it sometimes fails due to rate limits. You decide to use the @retry decorator from the tenacity library to avoid errors when possible."""

# Import the tenacity library
from tenacity import (retry, stop_after_attempt, wait_random_exponential)

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Add the appropriate parameters to the decorator
@retry(wait=wait_random_exponential(min=5, max=40), stop=stop_after_attempt(4))
def get_response(model, message):
    response = client.chat.completions.create(
      model=model,
      messages=[message]
    )
    return response.choices[0].message.content
print(get_response("gpt-4o-mini", {"role": "user", "content": "List ten holiday destinations."}))

"""Batching messages
You are developing a fitness application to track running and cycling training, but find out that all your customers' distances have been measured in kilometers, and you'd like to have them also converted to miles.

You decide to use the OpenAI API to send requests for each measurement, but want to avoid using a for loop that would send too many requests. You decide to send the requests in batches, specifying a system message that asks to convert each of the measurements from kilometers to miles and present the results in a table containing both the original and converted measurements.

The measurements list (containing a list of floats) and the get_response() function have already been imported."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

messages = []
# Provide a system message and user messages to send the batch
messages.append({
            "role": "system",
            "content": "Convert each measurement, given in kilometers, into miles, and reply with a table of all measurements."
        })
# Append measurements to the message
[messages.append({"role": "user", "content": str(i) }) for i in measurements]

response = get_response(messages)
print(response)

"""Setting token limits
An e-commerce platform just hired you to improve the performance of their customer service bot built using the OpenAI API. You've decided to start by ensuring that the input messages do not cause any rate limit issue by setting a limit of 100 tokens, and test it with a sample input message.

The tiktoken library has been preloaded."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")
input_message = {"role": "user", "content": "I'd like to buy a shirt and a jacket. Can you suggest two color pairings for these items?"}

# Use tiktoken to create the encoding for your model
encoding = tiktoken.encoding_for_model("gpt-4o-mini")
# Check for the number of tokens
num_tokens = len(encoding.encode(input_message['content']))

# Run the chat completions function and print the response
if num_tokens <= 100:
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[input_message])
    print(response.choices[0].message.content)
else:
    print("Message exceeds token limit")


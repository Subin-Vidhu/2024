'''Your first OpenAI API request!
To give you a taste of what's to come, the Python code to send a request to the OpenAI API has been set up for you.

Pass the prompt argument any prompt you wish to see how OpenAI's model responds. The prompt can be phrased as a question or instruction, so dive in and start prompting!

Here are a few prompts to try if you're struggling for ideas:

Simply and concisely, explain why learning about the OpenAI API is important for developers.
I work as a {insert your job title}. Give me three concise suggestions for tasks that could be automated with the OpenAI API.
In two sentences, how can the OpenAI API be used to upskill myself?'''

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    # Write your prompt
    messages=[{"role": "user", "content": "Who developed ChatGPT?"}],
    max_tokens=200
)

print(response.choices[0].message.content)

'''
Building an OpenAI API request
Throughout the course, you'll write Python code to interact with the OpenAI API. Entering your own API key is not necessary to create requests and complete the exercises in this course.

The OpenAI class has already been imported for you from the openai library.
'''

# Create the OpenAI client
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
  # Specify the correct model
  model="gpt-4o-mini",
  messages=[{"role": "user", "content": "Who developed ChatGPT?"}]
)

print(response)
'''
Digging into the response
One of the key skills required to work with APIs is manipulating the response to extract the desired information. In this exercise, you'll push your Python dictionary and list manipulation skills to the max to extract information from the API response.

You've been provided with response, which is a response from the OpenAI API when provided with the prompt, Who developed ChatGPT?

This response object has been printed for you so you can see and understand its structure.'''

# Extract the model from response
print(response.model)

# Extract the total_tokens from response
print(response.usage.total_tokens)

# Extract the text from response
print(response.choices[0].message.content)




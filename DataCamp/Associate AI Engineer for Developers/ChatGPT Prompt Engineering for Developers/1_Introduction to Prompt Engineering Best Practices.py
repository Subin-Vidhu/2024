"""OpenAI API message roles
You are developing a chatbot for an event management agency that will be used to facilitate networking during events.

Using the OpenAI API, you prepare a dictionary to pass as the message to the chat.completions endpoint. The message needs to have 3 roles defined to ensure the model has enough guidance to provide helpful responses.

Throughout the course, you'll write Python code to interact with the OpenAI API. Entering your own API key is not necessary to create requests and complete the exercises in this course. You can leave the placeholder "<OPENAI_API_TOKEN>" as the key in api_key."""

# Create the OpenAI client: you can leave "<OPENAI_API_TOKEN>" as is
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define the conversation messages
conversation_messages = [
    {"role": "system", "content": "You are a helpful event management assistant."},
    {"role": "user", "content": "What are some good conversation starters at networking events?"},
    {"role": "assistant", "content": ""}
]

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=conversation_messages
)
print(response.choices[0].message.content)
"""
Creating the get_response() function
Most of the exercises in this course will call the chat.completions endpoint of the OpenAI API with a user prompt. Here, you will create a get_response() function that receives a prompt as input and returns the response as an output, which in future exercises will be pre-loaded for you.

The OpenAI package, and OpenAI API Python client have been pre-loaded."""

def get_response(prompt):
  # Create a request to the chat completions endpoint
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}], 
    temperature = 0)
  return response.choices[0].message.content

# Test the function with your prompt
response = get_response("Write a poem about ChatGPT")
print(response)
"""
Exploring prompt engineering
Prompt engineering refers to crafting effective prompts to guide the language model towards the intended response. By refining your prompts, you can achieve better results and guide the model towards generating more accurate and useful responses. Your task in this exercise is to modify the prompt you used in the previous exercise.

The OpenAI package and the get_response() function have been pre-loaded for you."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a prompt that follows the instructions
prompt = "Write a poem about ChatGPT. Use basic English that a child can understand."

# Get the response
response = get_response(prompt)

print(response)
"""
Is this prompt effective?
Prompt engineering is about creating clear and concise prompts that guide the behavior of a language model efficiently to produce the desired output. In the previous video, you have learned about prompt engineering principles and what makes a prompt effective. Now, it's time to put your knowledge into practice!"""
"""
Using delimited prompts with f-strings
You are a junior developer at a dynamic startup that generates content with the help of AI. The company believes this technology can revolutionize storytelling, and you are excited to be a part of it. Today, your task is to generate a continuation of a story with a delimited prompt using an f-string.

The OpenAI package, the get_response() function, and the story variable have been pre-loaded for you."""


client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a prompt that completes the story
prompt = f"""Complete the story delimited by triple backticks. 
 ```{story}```"""

# Get the generated response 
response = get_response(prompt)

print("\n Original story: \n", story)
print("\n Generated story: \n", response)
"""
Building specific and precise prompts
In the previous exercise, you generated text that completes a given story. Your team was happy with your achievement, however, they want you to follow specific guidelines when it comes to length and style. Your task now is to craft a more specific prompt that controls these aspects of the generated story.

The OpenAI package, the get_response() function, and the same story variable have been pre-loaded for you."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a request to complete the story
prompt = f"""Complete the story delimited by triple backticks with only two paragraphs using the style of Shakespeare. 
 ```{story}```"""

# Get the generated response
response = get_response(prompt)

print("\n Original story: \n", story)
print("\n Generated story: \n", response)
"""
Generating a table
Imagine you are a developer working for a renowned online bookstore known for its extensive collection of science fiction novels. Today, you have a task at hand: to create a table of ten must-read science fiction books for the website's homepage. This will enhance the user experience on the website, helping fellow sci-fi enthusiasts discover their next great read."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a prompt that generates the table
prompt = "Generate a table containing 10 books I should read if I am a science fiction lover, with columns for Title, Author, and Year."

# Get the response
response = get_response(prompt)
print(response)
"""
Customizing output format
You work as a developer at a startup that offers a text analysis platform for content creators. Your platform helps users automatically categorize and format their content, and you're now working on a new feature that detects the language of a given piece of text and generates a suitable title for that text in a custom format. You decide to craft a prompt that guides the language model through this."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create the instructions
instructions = "You will be provided with a text delimited by triple backticks. Infer its language, then generate a suitable title for it. "

# Create the output format
output_format = """Use the following format for the output:
         - Text: <the text>
         - Language: <the text language>
         - Title: <the generated title>"""

# Create the final prompt
prompt = instructions + output_format + f"```{text}```"
response = get_response(prompt)
print(response)
"""
Using conditional prompts
Building upon the previous task, your next challenge is to enhance the responses you received. When processing a given text, you need to determine its language, count the number of sentences, and generate a suitable title if the text contains more than one sentence. However, here's the new twist: if the text consists of only one sentence, no title should be generated, and instead, the model should display "N/A". This modification ensures that the title is generated only for texts with multiple sentences, providing a more refined and practical output for your platform's users."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create the instructions
instructions = "You will be provided with a text delimited by triple backticks. Infer its language and the number of sentences it contains. Then, if the text has more than one sentence, generate a suitable title for it. Otherwise, if the text contains only one sentence, write 'N/A' for the title."

# Create the output format
output_format = """The output should follow this format:
          - Text: <the given text>
          - Language: <the text language>
          - Title: <the generated title, or N/A>'."""

prompt = instructions + output_format + f"```{text}```"
response = get_response(prompt)
print(response)


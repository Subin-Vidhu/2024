"""Find and replace
Text completion models can be used for much more than answering questions. In this exercise, you'll explore the model's ability to transform a text prompt.

Find-and-replace tools have been around for decades, but they are often limited to identifying and replacing exact words or phrases. You've been provided with a block of text discussing cars, and you'll use a completion model to update the text to discuss planes instead, updating the text appropriately.

Warning: if you send many requests or use lots of tokens in a short period, you may hit your rate limit and see an openai.error.RateLimitError. If you see this error, please wait a minute for your quota to reset and you should be able to begin sending more requests."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

prompt="""Replace car with plane and adjust phrase:
A car is a vehicle that is typically powered by an internal combustion engine or an electric motor. It has four wheels, and is designed to carry passengers and/or cargo on roads or highways. Cars have become a ubiquitous part of modern society, and are used for a wide variety of purposes, such as commuting, travel, and transportation of goods. Cars are often associated with freedom, independence, and mobility."""

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role": "user", "content": prompt}],
  max_tokens=100
)

# Extract and print the response text
print(response.choices[0].message.content)

# output: A plane is a vehicle that is typically powered by jet engines or propellers. It is designed to carry passengers and/or cargo through the air. Planes have become a ubiquitous part of modern society and are used for a wide variety of purposes, such as travel, logistics, and transportation of goods. Planes are often associated with freedom, adventure, and global connectivity.

'''
Text summarization
One really common use case for using OpenAI's models is summarizing text. This has a ton of applications in business settings, including summarizing reports into concise one-pagers or a handful of bullet points, or extracting the next steps and timelines for different stakeholders.
'''

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

prompt="""Summarize the following text into two concise bullet points:
Investment refers to the act of committing money or capital to an enterprise with the expectation of obtaining an added income or profit in return. There are a variety of investment options available, including stocks, bonds, mutual funds, real estate, precious metals, and currencies. Making an investment decision requires careful analysis, assessment of risk, and evaluation of potential rewards. Good investments have the ability to produce high returns over the long term while minimizing risk. Diversification of investment portfolios reduces risk exposure. Investment can be a valuable tool for building wealth, generating income, and achieving financial security. It is important to be diligent and informed when investing to avoid losses."""

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role": "user", "content": prompt}],
  max_tokens=400,
  temperature=0.5
)

print(response.choices[0].message.content)

# output: 
# - Investment involves committing capital to various options (e.g., stocks, bonds, real estate) with the expectation of profit, necessitating careful analysis of risks and rewards.
# - Diversifying investment portfolios can minimize risk exposure and is essential for building wealth and achieving financial security, emphasizing the importance of informed decision-making.

'''
Content generation
AI is playing a much greater role in content generation, from creating marketing content such as blog post titles to creating outreach email templates for sales teams.

In this exercise, you'll harness AI through the Chat Completions endpoint to generate a catchy slogan for a new restaurant. Feel free to test out different prompts, such as varying the type of cuisine (e.g., Italian, Chinese) or the type of restaurant (e.g., fine-dining, fast-food), to see how the response changes.'''

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role": "user", "content": "Create a slogan for a new restaurant."}],
  max_tokens=100
)

print(response.choices[0].message.content)

# output: "Flavor Awaits: Savor Every Bite!"

"""Classifying text sentiment
As well as answering questions, transforming text, and generating new text, OpenAI's models can also be used for classification tasks, such as categorization and sentiment classification. This sort of task requires not only knowledge of the words but also a deeper understanding of their meaning.

In this exercise, you'll explore using Chat Completions models for sentiment classification using reviews from an online shoe store called Toe-Tally Comfortable:

Unbelievably good!
Shoes fell apart on the second use.
The shoes look nice, but they aren't very comfortable.
Can't wait to show them off!"""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define a multi-line prompt to classify sentiment
prompt = """Classify sentiment as negative, positive, or neutral:
1. Unbelievably good!
2. Shoes fell apart on the second use.
3. The shoes look nice, but they aren't very comfortable.
4. Can't wait to show them off!"""

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role": "user", "content": prompt}],
  max_tokens=100
)

print(response.choices[0].message.content)
"""
Categorizing companies
In this exercise, you'll use a Chat Completions model to categorize different companies. At first, you won't specify the categories to see how the model categorizes them. Then, you'll specify the categories in the prompt to ensure they are categorized in a desirable and predictable way."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define a prompt for the categorization
prompt = "Categorize the following list of companies as either Tech, Energy, Luxury Goods, or Investment: Apple, Microsoft, Saudi Aramco, Alphabet, Amazon, Berkshire Hathaway, NVIDIA, Meta, Tesla, LVMH"

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
 model="gpt-4o-mini",
 messages=[{"role": "user", "content": prompt}],
 max_tokens=100,
 temperature=0.5
)

print(response.choices[0].message.content)

"""Chat Completions roles
The Chat Completions endpoint supports three different roles to shape the messages sent to the model:

System: controls assistant's behavior
User: instruct the assistant
Assistant: response to user instruction
In this exercise, you'll make a request to the Chat Completions endpoint, including a system messages, to answer the following question:

What is the difference between a for loop and a while loop?"""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
  model="gpt-4o-mini",
  max_tokens=150,
  messages=[
    {"role": "system",
     "content": "You are a helpful data science tutor."},
    {"role": "user",
     "content": "What is the difference between a for loop and a while loop?"}
  ]
)

# Extract the assistant's text response
print(response.choices[0].message.content)

"""Code explanation
One of the most popular use cases for using OpenAI models is for explaining complex content, such as technical jargon and code. This is a task that data practitioners, software engineers, and many others must tackle in their day-to-day as they review and utilize code written by others.

In this exercise, you'll use the OpenAI API to explain a block of Python code to understand what it is doing."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

instruction = """Explain what this Python code does in one sentence:
import numpy as np

heights_dict = {"Mark": 1.76, "Steve": 1.88, "Adnan": 1.73}
heights = heights_dict.values()
print(np.mean(heights))
"""

# Create a request to the Chat Completions endpoint
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful Python programming assistant."},
    {"role": "user", "content": instruction}
  ],
  max_tokens=100
)

print(response.choices[0].message.content)

# output: This Python code imports the NumPy library, creates a dictionary of heights, extracts the height values, and then calculates and prints the average height of the individuals in the dictionary.

"""In-context learning
For more complex use cases, the models lack the understanding or context of the problem to provide a suitable response from a prompt. In these cases, you need to provide examples to the model for it to learn from, so-called in-context learning.

In this exercise, you'll improve on a Python programming tutor built on the OpenAI API by providing an example that the model can learn from.

Here is an example of a user and assistant message you can use, but feel free to try out your own:

User → Explain what the min() Python function does.
Assistant → The min() function returns the smallest item from an iterable."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response = client.chat.completions.create(
   model="gpt-4o-mini",
   # Add a user and assistant message for in-context learning
   messages=[
     {"role": "system", "content": "You are a helpful Python programming tutor."},
     {"role": "user", "content": "Explain what the min() function does."},
     {"role": "assistant", "content": "The min() function returns the smallest item from an iterable."},
     {"role": "user", "content": "Explain what the type() function does."}
   ]
)

print(response.choices[0].message.content)

"""Creating an AI chatbot
An online learning platform called Easy as Pi that specializes in teaching math skills has contracted you to help develop an AI tutor. You immediately see that you can build this feature on top of the OpenAI API, and start to design a simple proof-of-concept (POC) for the major stakeholders at the company. This POC will demonstrate the core functionality required to build the final feature and the power of the OpenAI's GPT models.

Example system and user messages have been provided for you, but feel free to play around with these to change the model's behavior or design a completely different chatbot!"""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

messages = [{"role": "system", "content": "You are a helpful math tutor."}]
user_msgs = ["Explain what pi is.", "Summarize this in two bullet points."]

for q in user_msgs:
    print("User: ", q)
    
    # Create a dictionary for the user message from q and append to messages
    user_dict = {"role": "user", "content": q}
    messages.append(user_dict)
    
    # Create the API request
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=100
    )
    
    # Convert the assistant's message to a dict and append to messages
    assistant_dict = {"role": "assistant", "content": response.choices[0].message.content}
    messages.append(assistant_dict)
    print("Assistant: ", response.choices[0].message.content, "\n")

# User:  Explain what pi is.
#     Assistant:  Pi, represented by the symbol \( \pi \), is a mathematical constant that represents the ratio of a circle's circumference to its diameter. This means that for any circle, if you measure the distance around it (the circumference) and divide that by the distance across it (the diameter), you will always get the same value: approximately 3.14159. 
    
#     Pi is an irrational number, which means it cannot be exactly expressed as a simple fraction. Its decimal representation goes on forever without repeating 
    
#     User:  Summarize this in two bullet points.
#     Assistant:  - Pi (\( \pi \)) is the constant ratio of a circle's circumference to its diameter, approximately equal to 3.14159.
#     - It is an irrational number, meaning its decimal representation is infinite and non-repeating. 


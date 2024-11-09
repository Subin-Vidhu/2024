"""Zero-shot, one-shot, and few-shot prompting
Learning from examples is necessary to improve the performance of a language model on a given task. According to the number of examples (question-answer pairs) provided in the prompt, you differentiate between zero-shot, one-shot, and few-shot prompts. In this exercise, you will be given a set of prompts and your job is to classify them between the three categories."""
"""
Controlling output structure
One way to control the output structure provided by a language model is to give it a sample question-answer in the prompt. The model will learn from it and follow it when generating responses for similar questions. This exercise aims to let you build a one-shot prompt that extracts odd numbers from a given set of numbers and displays them as a set of numbers between brackets, separated by commas as shown in the instructions."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a one-shot prompt
prompt = """
     Q: Extract the odd numbers from {1, 3, 7, 12, 19}. A: Odd numbers = {1, 3, 7, 19}
     Q: Extract the odd numbers from {3, 5, 11, 12, 16}. A:
"""

response = get_response(prompt)
print(response)
"""
Sentiment analysis with few-shot prompting
You're working on market research and your goal is to use few-shot prompting to perform sentiment analysis on customer reviews. You are assigning a number for a given customers conversation: -1 if the sentiment is negative, 1 if positive. You provide the following examples as previous conversations for the model to learn from.

The product quality exceeded my expectations -> 1
I had a terrible experience with this product's customer service -> -1"""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response = client.chat.completions.create(
  model = "gpt-4o-mini",
  # Provide the examples as previous conversations
  messages = [{"role": "user",
  		     "content": "The product quality exceeded my expectations"},
              {"role": "assistant",
  		     "content": "1"},
              {"role": "user",
  		     "content": "I had a terrible experience with this product's customer service"},
              {"role": "assistant",
  		     "content": "-1"}, 
              # Provide the text for the model to classify
              {"role": "user",
  		     "content": "The price of the product is really fair given its features"}
             ],
  temperature = 0
)
print(response.choices[0].message.content)

"""
Single-step prompt to plan a trip
Imagine you're a developer taking a break and you want to apply your prompting skills to plan the perfect beach vacation. As an initial step, you decide to use a standard single-step prompt to seek assistance.

The OpenAI package and the get_response() function have been pre-loaded for you."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a single-step prompt to get help planning the vacation
prompt = "Help me plan a beach vacation."

response = get_response(prompt)
print(response)
"""
Multi-step prompt to plan a trip
You noticed that the single-step prompt was not effective, because the answer was too vague for what you had in mind. You improve your prompt by specifying the steps to follow for planning. The plan should have four potential locations for your beach vacation, and each location should have some accommodation options, some activities, and an evaluation of the pros and cons."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a prompt detailing steps to plan the trip
prompt = """
     Help me plan a beach vacation.
     Step 1 - Specify four potential locations for beach vacations
     Step 2 - State some accommodation options in each
     Step 3 - State activities that could be done in each
     Step 4 - Evaluate the pros and cons for each destination
    """

response = get_response(prompt)
print(response)
"""
Analyze solution correctness
You're back from your relaxing vacation and you've been assigned the task of reviewing and correcting some programming tasks, including a function to calculate of the area of a shape. You are provided with a code string that contains the function to calculate the area of a rectangle, and need to assess its correctness. The ideal function for you is a function that has correct syntax, receives two inputs, and returns one output."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

code = '''
def calculate_rectangle_area(length, width):
    area = length * width
    return area
'''

# Create a prompt that analyzes correctness of the code
prompt = f"""
     Analyze the correctness of the function delimited by triple backticks according to the following criteria:
      1- It should have correct syntax
      2- The function should receive only 2 inputs
      3- The function should return only one output
      ```{code}```
    """

response = get_response(prompt)
print(response)

"""Reasoning with chain-of-thought prompts
Chain-of-thought prompting is helpful to explain the reasoning behind the answer that the model is giving, especially in complex tasks such as generating the solution for a mathematical problem or a riddle. In this exercise, you will craft a chain-of-thought prompt to let the language model guess the age of your friend's father based on some information you will provide."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create the chain-of-thought prompt
prompt = "Compute the age of my friend's father in 10 years, given that now he's double my friend's age, and my friend is 20. Give a step by step explanation."

response = get_response(prompt)
print(response)

"""One-shot chain-of-thought prompts
When you need to sum the even numbers within a given set, you first have to identify these even numbers and then sum them. You can teach this to a language model via one or more examples, and it will follow this strategy to operate on new sets.

Your goal in this exercise is to teach the model how to apply this procedure on the following set: {9, 10, 13, 4, 2}, and then ask the model to perform it on a new set: {15, 13, 82, 7, 14}. This is how you perform chain-of-thought prompting through one-shot prompting."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define the example 
example = """Q: Sum the even numbers in the following set: {9, 10, 13, 4, 2}.
             A: Even numbers: 10, 4, 2. Adding them: 10+4+2=16"""

# Define the question
question = """Q: Sum the even numbers in the following set: {15, 13, 82, 7, 14} 
             A:"""

# Create the final prompt
prompt = example + question
response = get_response(prompt)
print(response)

"""Self-consistency prompts
Imagine you own a store that sells laptops and mobile phones. You start your day with 50 devices in the store, out of which 60% are mobile phones. Throughout the day, three clients visited the store, each of them bought one mobile phone, and one of them bought additionally a laptop. Also, you added to your collection 10 laptops and 5 mobile phones. How many laptops and mobile phones do you have by the end of the day? This problem is defined in the problem_to_solve string, and you will use a self-consistency prompt to solve it."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create the self_consistency instruction
self_consistency_instruction = "Imagine three completely independent experts who reason differently are answering this question. The final answer is obtained by majority vote. The question is: "

# Create the problem to solve
problem_to_solve = "If you own a store that sells laptops and mobile phones. You start your day with 50 devices in the store, out of which 60% are mobile phones. Throughout the day, three clients visited the store, each of them bought one mobile phone, and one of them bought additionally a laptop. Also, you added to your collection 10 laptops and 5 mobile phones. How many laptops and mobile phones do you have by the end of the day?"

# Create the final prompt
prompt = self_consistency_instruction + problem_to_solve

response = get_response(prompt)
print(response)
"""
Iterative prompt engineering process
No prompt can be perfect at the beginning, which is why prompt engineering is considered an iterative process in which you keep updating and refining your prompts to get the desired output."""

"""Iterative prompt engineering for standard prompts
You are a developer using prompt engineering techniques for your various tasks, and you want to carefully select the right language model. You wrote an initial prompt to know what are the top ten pre-trained language models out there. Now, your goal is to refine this prompt to generate a table presenting information on each model's name, release year and its owning company."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Refine the following prompt
prompt = "Generate a table that contains the top 10 pre-trained language models, with columns for language model, release year, and owners."

response = get_response(prompt)
print(response)

# Here’s a table containing the top 10 pre-trained language models, along with their release years and owners:
    
#     | Language Model         | Release Year | Owners/Developers          |
#     |------------------------|--------------|-----------------------------|
#     | BERT                   | 2018         | Google                      |
#     | GPT-2                  | 2019         | OpenAI                     |
#     | RoBERTa                | 2019         | Facebook AI Research        |
#     | T5                     | 2019         | Google                      |
#     | GPT-3                  | 2020         | OpenAI                     |
#     | XLNet                  | 2019         | Google/CMU                 |
#     | ALBERT                 | 2019         | Google                      |
#     | ELECTRA                | 2020         | Google                      |
#     | CLIP                   | 2021         | OpenAI                     |
#     | PaLM                   | 2022         | Google                      |
"""
Iterative prompt engineering for few-shot prompts
You are currently working on a project at your content creation company. The project's objective is to develop a text classification model capable of accurately identifying and categorizing different emotions in text, such as happiness, sadness, and fear. In cases where the text does not contain any discernible emotion, you aim for the model to respond with "no explicit emotion."

You decided to use the provided few-shot prompt. However, you've noticed that "Time flies like an arrow" is being incorrectly classified as "surprise." Your objective now is to refine the prompt so that the model correctly classifies this particular example as "no explicit emotion."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Refine the following prompt
prompt = """
Receiving a promotion at work made me feel on top of the world -> Happiness
The movie's ending left me with a heavy feeling in my chest -> Sadness
Walking alone in the dark alley sent shivers down my spine -> Fear
School begins tomorrow -> No explicit emotion
He painted the fence blue -> No explicit emotion
They sat and ate their meal ->
"""

response = get_response(prompt)
print(response)


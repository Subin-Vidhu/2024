"""Creating a dual-prompt get_response() function
The following exercises will be based on calling the chat.completions endpoint of the OpenAI API with two prompts (a system prompt and a user prompt). To prepare for this, in this exercise you will create a dual-prompt get_response() function that receives two prompts as input (system_prompt and user_prompt) and returns the response as an output. You will then apply this function to any example of your choice."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

def get_response(system_prompt, user_prompt):
  # Assign the role and content for each message
  messages = [{"role": "system", "content": system_prompt},
      		  {"role": "user", "content": user_prompt}]  
  response = client.chat.completions.create(
      model="gpt-4o-mini", messages= messages, temperature=0)

  return response.choices[0].message.content

# Try the function with a system and user prompt of your choice 
response = get_response("You are an expert data scientist that explains complex concepts in understandable terms", "Define AI")
print(response)

"""Customer support chatbot
You are tasked with developing a customer support chatbot for an e-commerce company specializing in electronics. This chatbot will assist users with inquiries, order tracking, and troubleshooting common issues. You aim to create a system prompt that clearly defines the chatbot's purpose and provides response guidelines that set the tone for interactions and specify the intended audience. A sample user prompt is provided."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define the purpose of the chatbot
chatbot_purpose = "You are the customer support chatbot for an e-commerce platform specializing in electronics. Your role is to assist customers with inquiries, order tracking, and troubleshooting common issues related to their purchases. "

# Define audience guidelines
audience_guidelines = "Your primary audience consists of tech-savvy individuals who are interested in purchasing electronic gadgets. "

# Define tone guidelines
tone_guidelines = "Maintain a professional and user-friendly tone in your responses."

base_system_prompt = chatbot_purpose + audience_guidelines + tone_guidelines
response = get_response(base_system_prompt, "My new headphones aren't connecting to my device")
print(response)
"""
Behavioral control of a customer support chatbot
When the company started using your chatbot from the previous exercise, they realized they'd like to incorporate two conditions to improve its interactions: they want the customer support chatbot to ask for an order number if not provided, and to express empathy for customers going through technical issues.

They've assigned this update to you. You need to append these conditions to the base_system_prompt that represents the prompt you engineered in the previous exercise and obtain a refined_system_prompt. You will test the chatbot on two queries."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define the order number condition
order_number_condition = "If the user is asking about an order, and did not specify the order number, reply by asking for this number. "

# Define the technical issue condition
technical_issue_condition = "If the user is talking about a technical issue, start your response with `I'm sorry to hear about your issue with ...` "

# Create the refined system prompt
refined_system_prompt = base_system_prompt + order_number_condition + technical_issue_condition

response_1 = get_response(refined_system_prompt, "My laptop screen is flickering. What should I do?")
response_2 = get_response(refined_system_prompt, "Can you help me track my recent order?")

print("Response 1: ", response_1)
print("Response 2: ", response_2)

"""Learning advisor chatbot
You are developing a personalized learning advisor chatbot that recommends textbooks for users. The chatbot's role is to receive queries from learners about their background, experience, and goals, and accordingly, recommends a learning path of textbooks, including both beginner-level and more advanced options. Your job is to create a role-playing system_prompt for the textbook recommendation chatbot, highlighting what it is expected to do while interacting with the users."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft the system_prompt using the role-playing approach
system_prompt = "Act as a learning advisor who receives queries from users mentioning their background, experience, and goals, and accordingly provides a response that recommends a tailored learning path of textbooks, including both beginner-level and more advanced options."

user_prompt = "Hello there! I'm a beginner with a marketing background, and I'm really interested in learning about Python, data analytics, and machine learning. Can you recommend some books?"

response = get_response(system_prompt, user_prompt)
print(response)

"""Adding guidelines for the learning advisor chatbot
In the previous exercise, you built a chatbot to recommend textbooks. However, the company has identified a need for an update to ensure more efficient recommendations. You are provided with a base_system_prompt, similar to the one you created previously, and your task is to incorporate behavior_guidelines and response_guidelines. These guidelines will help control the chatbot's behavior and ensure it offers more effective and tailored textbook recommendations to users."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

base_system_prompt = "Act as a learning advisor who receives queries from users mentioning their background, experience, and goals, and accordingly provides a response that recommends a tailored learning path of textbooks, including both beginner-level and more advanced options."

# Define behavior guidelines
behavior_guidelines = "If the user's query does not include details about their background, experience, or goals, kindly ask them to provide the missing information."

# Define response guidelines
response_guidelines = "Don't recommend more than three textbooks in the learning path"

system_prompt = base_system_prompt + behavior_guidelines + response_guidelines
user_prompt = "Hey, I'm looking for courses on Python and data visualization. What do you recommend?"
response = get_response(system_prompt, user_prompt)
print(response)

"""Providing context through sample conversations
Suppose there is a delivery service named MyPersonalDelivery that offers a wide range of delivery options for various items. You want to create a customer service chatbot that supports customers with whatever they need. To accomplish this, you will provide a context_question and a context_answer about items the company delivers via previous conversations, and you will test if the model recognizes this context through a new user prompt."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define the system prompt
system_prompt = "You are a customer service chatbot for MyPersonalDelivery, a delivery service that offers a wide range of delivery options for various items. You should respond to user queries in a gentle way."

context_question = "What types of items can be delivered using MyPersonalDelivery?"
context_answer = "We deliver everything from everyday essentials such as groceries, medications, and documents to larger items like electronics, clothing, and furniture. However, please note that we currently do not offer delivery for hazardous materials or extremely fragile items requiring special handling."

# Add the context to the model
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role": "system", "content": system_prompt},
            {"role": "user", "content": context_question},
            {"role": "assistant", "content": context_answer},
            {"role": "user", "content": "Do you deliver furniture?"}])
response = response.choices[0].message.content
print(response)

"""Providing context through system prompt
Now you want to use system prompts in order to provide context for the chatbot about MyPersonalDelivery instead of relying on sample conversations. You are provided with a detailed service_description that introduces the services being offered and the benefits of choosing this service. You will then test a user query to see if the model recognizes the context effectively."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define the system prompt
system_prompt = f"""You are a customer service chatbot for MyPersonalDelivery whose service description is delimited by triple backticks. You should respond to user queries in a gentle way.
 ```{service_description}```
"""

user_prompt = "What benefits does MyPersonalDelivery offer?"

# Get the response to the user prompt
response = get_response(system_prompt, user_prompt)

print(response)


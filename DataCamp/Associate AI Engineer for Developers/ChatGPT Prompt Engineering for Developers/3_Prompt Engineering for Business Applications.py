"""Market research report summarization
A market research firm needs to analyze and summarize lengthy reports on market trends and customer behavior. They want to know how AI and data privacy are shaping the market and how they're affecting customers. You are provided with a report string about markets trends and how they're affecting customer behavior. Your goal is to craft a prompt to summarize it while focusing on aspects related to AI and data privacy to see their effect on customers."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a prompt to summarize the report
prompt = f"""
Summarize the report delimited by triple backticks with a maximum of 5 sentences, while focusing on aspects related to AI and data privacy.
 ```{report}```
"""

response = get_response(prompt)

print("Summarized report: \n", response)
"""
Product features summarization
An electronics review website wants to provide concise and easy-to-read summaries of product features for its readers, allowing them to compare and evaluate different products quickly. The review website wants to generate bullet-point summaries, and, to start with, they want you to craft a prompt that summarizes a product_description for a smartphone."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a prompt to summarize the product description
prompt = f"""
Summarize the product description delimited by triple backticks, in at most five bullet points.
 ```{product_description}```
"""

response = get_response(prompt)

print("Original description: \n", product_description)
print("Summarized description: \n", response)
"""
Product description expansion
As you continue your work on the electronics review website, you've come across some products that are already summarized but lack a comprehensive description. Your task now is to expand these concise product descriptions into detailed narratives, ensuring that each product has both a full description and a bulleted summary for easy comparison. The complete description should effectively capture the product's unique features, benefits, and potential applications. You will apply your first prompt on a smart home security camera's product description."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a prompt to expand the product's description
prompt = f"""
Expand the product description for the Smart Home Security Camera delimited by triple backticks to provide a comprehensive overview of its features, benefits, potential applications, without bypassing the limit of one paragraph. 
 ```{product_description}```
"""

response = get_response(prompt)

print("Original description: \n", product_description)
print("Expanded description: \n", response)

"""Translation for multilingual communication
A multinational company wants to expand its reach to more international markets. They need a language translation solution to convert their product descriptions and marketing materials into multiple languages. These will then be verified before being published.

Your task is to design a prompt that translates text from one language to multiple other languages, facilitating effective communication with customers worldwide. You will apply your prompt on a provided marketing_message that introduces their latest collection of premium leather handbags."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a prompt that translates
prompt = f"""Translate the English marketing message delimited by triple backticks to French, Spanish, and Japanese
 ```{marketing_message}```
"""

response = get_response(prompt)

print("English:", marketing_message)
print(response)

"""Tone adjustment for email marketing
An e-commerce company regularly conducts email marketing campaigns to promote its products, inform customers about new arrivals, and offer exclusive deals. The company has a hypothesis that its current strategy is too informal and wants to test out how tone adjustment to their emails could help boost customer engagement.

Your task is to craft a prompt that can effectively transform the tone of marketing emails. You will apply your prompt on the sample_email provided."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a prompt to change the email's tone
prompt = f"""
Write the email delimited by triple backticks using a professional, positive, and user-centric tone:
 ```{sample_email}```
"""

response = get_response(prompt)

print("Before transformation: \n", sample_email)
print("After transformation: \n", response)

"""Writing improvement
A popular online community relies on user-generated content to thrive. Users frequently contribute reviews, articles, and comments, but the quality of these contributions varies. To elevate the overall experience for its members, the community aims to enhance user-generated texts. This includes fixing grammar errors and refining writing tones to create a more polished and engaging environment for all users. Your task is to build a multi-step prompt that proofreads and adjusts the tone of a given text."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a prompt to transform the text
prompt = f"""Transform the text delimited by triple backticks with the following two steps:
Step 1 - Proofread it without changing its structure
Step 2 - Change the tone to be formal and friendly
 ```{text}```"""

response = get_response(prompt)

print("Before transformation:\n", text)
print("After transformation:\n", response)

"""Customer support ticket routing
A large customer support team receives many tickets related to different business areas, such as technical issues, billing inquiries, and product feedback. Your task is to create a prompt that automatically classifies incoming tickets into these three groups and routes them to the appropriate support specialists, reducing response times and enhancing customer satisfaction. You will test your prompt on a provided sample ticket."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a prompt to classify the ticket
prompt = f"""Classify the ticket delimited by triple backticks as technical issue, billing inquiry, or product feedback. Your response should just contain the class and nothing else.
 ```{ticket}```"""

response = get_response(prompt)

print("Ticket: ", ticket)
print("Class: ", response)

"""Customer support ticket analysis
The customer support team receive tickets through various channels, such as email, chat, and social media. The company wants to automatically extract key entities to categorize and prioritize the tickets appropriately. Your job is to craft a few-shot prompt that helps them achieve that.

You have three sample tickets (ticket_1, ticket_2, and ticket_3) and their corresponding entities (entities_1, entities_2, and entities_3) to inform the model on what to look for and how to display it. You need the model to extract entities from the new ticket_4 string."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a few-shot prompt to get the ticket's entities
prompt = f"""Ticket: {ticket_1} -> Entities: {entities_1}
            Ticket: {ticket_2} -> Entities: {entities_2}
            Ticket: {ticket_3} -> Entities: {entities_3}
            Ticket: {ticket_4} -> Entities: """

response = get_response(prompt)

print("Ticket: ", ticket_4)
print("Entities: ", response)

"""Code generation with problem description
You work as an analyst for a retail company and analyze monthly sales data. You need to develop a Python function that accepts a list of 12 numbers representing sales for each month of the year and outputs the month with the highest sales value. This information will help your company identify the most profitable month. You feed the problem description to a language model to get help."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a prompt that asks the model for the function
prompt = "Write a Python function that accepts a list of 12 numbers representing sales for each month of the year, and outputs the month with the highest sales value"

response = get_response(prompt)
print(response)

"""Input-output examples for code generation
You work as a project manager and need to estimate the time it will take to complete different projects. Your task is to develop a Python function that can predict the estimated completion time for a project based on historical data. You are given a set of examples in the examples string where different factors are associated with project completion time. Each example includes the factors' numerical values and the corresponding estimated completion time."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

examples="""input = [10, 5, 8] -> output = 23
input = [5, 2, 4] -> output = 11
input = [2, 1, 3] -> output = 6
input = [8, 4, 6] -> output = 18
"""

# Craft a prompt that asks the model for the function
prompt = f"""You are provided with input-output examples delimited by triple backticks for a Python function where different factors are associated with project completion time. Each example includes numerical values for the factors and the corresponding estimated completion time. Write code for this function.
 ```{examples}```"""

response = get_response(prompt)
print(response)

"""Modifying code with multi-step prompts
You are a home improvement contractor specializing in flooring installations. You need to develop a Python function that calculates the area and perimeter of a rectangular floor in a room to help you determine the amount of flooring material required for the project.

You are given a string named function, which contains a starter function that calculates the area of a rectangular floor given its width and length. Using a multi-step prompt, you need to prompt the language model to modify this function to return the perimeter of the rectangle as well, and to test if the inputs (floor dimensions) are positive, and if not, display appropriate error messages."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

function = """def calculate_area_rectangular_floor(width, length):
					return width*length"""

# Craft a multi-step prompt that asks the model to adjust the function
prompt = f"""Modify the script delimited by triple backticks as follows:
             - The function should return the perimeter of the rectangular floor as well.
             - The inputs (floor dimensions) should be positive. Otherwise, appropriate error messages should be displayed.
           ```{function}```"""

response = get_response(prompt)
print(response)

"""Explaining code step by step
As a financial analyst at a consulting firm, you're tasked with analyzing investment portfolios and providing insights to clients. While reviewing a set of financial data files, you come across a Python function that seems related to analyzing portfolios, but you're unsure of its exact purpose. You decide to use chain-of-thought prompting to let the language model decipher it step by step."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Craft a chain-of-thought prompt that asks the model to explain what the function does
prompt = f"""Explain what the function delimited by triple backticks does. Let's think step by step
 ```{function}```
"""
 
response = get_response(prompt)
print(response)


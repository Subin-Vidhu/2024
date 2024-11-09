"""Function calling steps
Function calling enables the use of custom functions as input to the OpenAI endpoint, resulting in improved consistency of the responses."""

"""Using the tools parameter
You are developing an AI application for a real estate agency and have been asked to extract some key data from listings: house type, location, price, number of bedrooms. Use the Chat Completions endpoint with function calling to extract the information.

The message_listing message, containing the real estate listing, and function_definition, containing the function to call defined as a tool to be passed to the model, have been preloaded."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response= client.chat.completions.create(
    model="gpt-4o-mini",
    # Add the message 
    messages=message_listing,
    # Add your function definition
    tools=function_definition
)

# Print the response
print(response.choices[0].message.tool_calls[0].function.arguments)

"""Building a function dictionary
You are working on a research project where you need to extract key information from a collection of scientific research papers. The goal is to create a summary of key information from the papers you are given, that includes the title and year of publication. To compile this, you decide to use the OpenAI API with function calling to extract the key information.

The get_response() function and messages, containing the text of the research paper, have been preloaded. The function_definition variable has also partially been filled already."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define the function parameter type
function_definition[0]['function']['parameters']['type'] = 'object'

# Define the function properties
function_definition[0]['function']['parameters']['properties'] = {'title': {'type': 'string',
      'description': 'Title of the research paper'},
     'year': {'type': 'string', 'description': 'Year of publication of the research paper'}}

response = get_response(messages, function_definition)
print(response)

"""Extracting the response
You work for a company that has just launched a new smartphone. The marketing team has collected customer reviews from various online platforms and wants to analyze the feedback to understand the customer sentiment and the most talked-about features of the smartphone. To accelerate this, you've used the OpenAI API to extract structured data from these reviews, using function calling. You now need to write a function to clean the output and return a dictionary of the response from the function only.

The get_response() function, messages variable (containing the review) and function_definition (containing the function to extract sentiment and product features from reviews) have been preloaded. Notice that both messages and function_definition can be passed as arguments to the get_response() function to get the response from the chat completions endpoint."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response = get_response(messages, function_definition)

# Define the function to extract the data dictionary
def extract_dictionary(response):
  return response.choices[0].message.tool_calls[0].function.arguments

# Print the data dictionary
print(extract_dictionary(response))

"""Parallel function calling
After extracting the data from customers' reviews for the marketing team, the company you're working for asks you if there's a way to generate a response to the customer that they can post on their review platform. You decide to use parallel function calling to apply both functions and generate data as well as the responses. You use a function named reply_to_review and ask to return the review reply as a reply property.

In this exercise, the get_response() function, messages and function_definition variable have been preloaded. The messages already contain the user's review, and function_definition contains the function asking to extract structured data."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Append the second function
function_definition.append({'type': 'function', 'function':{'name': 'reply_to_review', 'description': 'Reply politely to the customer who wrote the review', 'parameters': {'type': 'object', 'properties': {'reply': {'type': 'string','description': 'Reply to post in response to the review'}}}}})

response = get_response(messages, function_definition)

# Print the response
print(response)

"""Setting a specific function
You have been given a few customer reviews to analyze, and have been asked to extract for each one the product name, variant, and customer sentiment. To ensure that the model extracts this specific information, you decide to use function calling and specify the function for the model to use. Use the Chat Completions endpoint with function calling and tool_choice to extract the information.

In this exercise, the messages and function_definition have been preloaded."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

response= client.chat.completions.create(
    model=model,
    messages=messages,
    # Add the function definition
    tools=function_definition,
    # Specify the function to be called for the response
    tool_choice={"type": "function", "function": {"name": "extract_review_info"}}
)

# Print the response
print(response.choices[0].message.tool_calls[0].function.arguments)

"""Avoiding inconsistent responses
The team you were working with on the previous project is enthusiastic about the reply generator and asks you if more reviews can be processed. However, some reviews have been mixed up with other documents, and you're being asked not to return responses if the text doesn't contain a review, or relevant information. For example, the review you're considering now doesn't contain a product name, and so there should be no product name being returned.

In this exercise, the get_response() function, and messages and function_definition variables have been preloaded. The messages already contain the user's review, and function_definition contains the two functions: one asking to extract structured data, and one asking to generate a reply."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Modify the messages
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions."})

response = get_response(messages, function_definition)

print(response)

"""Defining a function with external APIs
You are developing a flight simulation application and have been asked to develop a system that provides specific information about airports mentioned in users' requests. You decide to use the OpenAI API to convert the user request into airport codes, and then call the AviationAPI to return the information requested. As the first step in your coding project, you configure the function to pass to the tools parameter in the Chat Completions endpoint."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Define the function to pass to tools
function_definition = [{"type": "function",
                        "function" : {"name": "get_airport_info",
                                      "description": "This function calls the Aviation API to return the airport code corresponding to the airport in the request",
                                      "parameters": {"type": "object",
                                                     "properties": {"airport_code": {"type": "string","description": "The code to be passed to the get_airport_info function."}} }, 
                                      "result": {"type": "string"} } } ]

response = get_response(function_definition)
print(response)

"""Calling an external API
Now that you have a clearly structured function definition, you move on to improving your endpoint request. You use the Chat Completions endpoint and pass a system message to ensure that the AI assistant is aware that it is in the aviation space and that it needs to extract the corresponding airport code based on the user input."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Call the Chat Completions endpoint 
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{
    "role": "system",
    "content": "You are an AI assistant, an aviation specialist. You should interpret the user prompt, and based on it extract an airport code corresponding to their message."},
    {"role": "user", "content": "I'm planning to land a plane in JFK airport in New York and would like to have the corresponding information."}],
  tools=function_definition)

print_response(response)

"""Handling the response with external API calls
To better connect your flight simulation application to other systems, you'd like to add some checks to make sure that the model has found an appropriate answer. First you check that the response has been produced via tool_calls. If that is the case, you check that the function used to produce the result was get_airport_info. If so, you load the airport code extracted from the user's prompt, and call the get_airport_info() function with the code as argument. Finally, if that produces a response, you return the response."""

# Check that the response has been produced using function calling
if response.choices[0].finish_reason=='tool_calls':
# Extract the function
    function_call = response.choices[0].message.tool_calls[0].function
    print(function_call)
else: 
    print("I am sorry, but I could not understand your request.")

    
"""Handling the response with external API calls
To better connect your flight simulation application to other systems, you'd like to add some checks to make sure that the model has found an appropriate answer. First you check that the response has been produced via tool_calls. If that is the case, you check that the function used to produce the result was get_airport_info. If so, you load the airport code extracted from the user's prompt, and call the get_airport_info() function with the code as argument. Finally, if that produces a response, you return the response."""

if response.choices[0].finish_reason=='tool_calls':
  function_call = response.choices[0].message.tool_calls[0].function
  # Check function name
  if function_call.name == "get_airport_info":
    # Extract airport code
    code = json.loads(function_call.arguments)["airport code"]
    airport_info = get_airport_info(code)
    print(airport_info)
  else:
    print("Apologies, I couldn't find any airport.")
else: 
  print("I am sorry, but I could not understand your request.")


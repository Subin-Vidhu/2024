"""Building prompts for sequential chains
Over the next couple of exercises, you'll work to create a system for helping people learn new skills. This system needs to be built sequentially, so learners can modify plans based on their preferences and constraints. You'll utilize your LangChain LCEL skills to build a sequential chain to build this system, and the first step is to design the prompt templates that will be used by this system."""

# Create a prompt template that takes an input activity
learning_prompt = PromptTemplate(
    input_variables=["activity"],
    template="I want to learn how to {activity}. Can you suggest how I can learn this step-by-step?"
)

# Create a prompt template that places a time constraint on the output
time_prompt = PromptTemplate(
    input_variables=["learning_plan"],
    template="I only have one week. Can you create a plan to help me hit this goal: {learning_plan}."
)

# Invoke the learning_prompt with an activity
print(learning_prompt.invoke({"activity": "play golf"}))

"""Sequential chains with LCEL
With your prompt templates created, it's time to tie everything together, including the LLM, using chains and LCEL. An llm has already been defined for you that uses OpenAI's gpt-4o-mini model

For the final step of calling the chain, feel free to insert any activity you wish! If you're struggling for ideas, try inputting "play the harmonica"."""

learning_prompt = PromptTemplate(
    input_variables=["activity"],
    template="I want to learn how to {activity}. Can you suggest how I can learn this step-by-step?"
)

time_prompt = PromptTemplate(
    input_variables=["learning_plan"],
    template="I only have one week. Can you create a plan to help me hit this goal: {learning_plan}."
)

# Complete the sequential chain with LCEL
seq_chain = ({"learning_plan": learning_prompt | llm | StrOutputParser()}
    | time_prompt
    | llm
    | StrOutputParser())

# Call the chain
print(seq_chain.invoke({"activity": "play the harmonica"}))

"""ReAct agents
Time to have a go at creating your own ReAct agent! Recall that ReAct stands for Reason and Act, which describes how they make decisions. In this exercise, you'll load the built-in wikipedia tool to integrate external data from Wikipedia with your LLM. An llm has already been defined for you that uses OpenAI's gpt-4o-mini model

Note: The wikipedia tool requires the wikipedia Python library to be installed as a dependency, which has been done for you in this case."""

# Define the tools
tools = load_tools(["wikipedia"])

# Define the agent
agent = create_react_agent(llm, tools)

# Invoke the agent
response = agent.invoke({"messages": [("human", "How many people live in New York City?")]})
print(response['messages'][-1].content)

"""Defining a function for tool use
You're working for a SaaS (software as a service) company with big goals for rolling out tools to help employees at all levels of the organization to make data-informed decisions. You're creating a PoC for an application that allows customer success managers to interface with company data using natural language to retrieve important customer data.

You've been provided with a pandas DataFrame called customers that contains a small sample of customer data. Your first step in this project is to define a Python function to extract information from this table given a customer's name. pandas has already been imported as pd."""

# Define a function to retrieve customer info by-name
def retrieve_customer_info(name: str) -> str:
    """Retrieve customer information based on their name."""
    # Filter customers for the customer's name
    customer_info = customers[customers['name'] == name]
    return customer_info.to_string()
  
# Call the function on Peak Performance Co.
print(retrieve_customer_info("Peak Performance Co."))

"""Creating custom tools
Now that you have a function for extracting customer data from the customers DataFrame, it's time to convert this function into a tool that's compatible with LangChain agents."""

# Convert the retrieve_customer_info function into a tool
@tool
def retrieve_customer_info(name: str) -> str:
    """Retrieve customer information based on their name."""
    customer_info = customers[customers['name'] == name]
    return customer_info.to_string()
  
# Print the tool's arguments
print(retrieve_customer_info.args)

"""Integrating custom tools with agents
Now that you have your tools at-hand, it's time to set up your agentic workflow! You'll again be using a ReAct agent, which, recall, reasons on the steps it should take, and selects tools using this context and the tool descriptions. An llm has already been defined for you that uses OpenAI's gpt-4o-mini model"""

@tool
def retrieve_customer_info(name: str) -> str:
    """Retrieve customer information based on their name."""
    customer_info = customers[customers['name'] == name]
    return customer_info.to_string()

# Create a ReAct agent
agent = create_react_agent(llm, [retrieve_customer_info])

# Invoke the agent on the input
messages = agent.invoke({"messages": [("human", "Create a summary of our customer: Peak Performance Co.")]})
print(messages['messages'][-1].content)


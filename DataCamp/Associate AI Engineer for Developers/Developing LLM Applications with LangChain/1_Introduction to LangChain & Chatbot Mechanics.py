"""
Hugging Face models in LangChain!
There are thousands of language models freely available to use on Hugging Face. Hugging Face integrates really nicely into LangChain, so in this exercise, you'll use LangChain to load and predict using a model from Hugging Face.

To complete this exercise, you'll need first need to create a free Hugging Face API token.

Sign up for a Hugging Face account at https://huggingface.co/join
Navigate to https://huggingface.co/settings/tokens
Select "New token" and copy the key
"""

from langchain_huggingface import HuggingFaceEndpoint

# Set your Hugging Face API token 
huggingfacehub_api_token = '<HUGGING_FACE_TOKEN>'

# Define the LLM
llm = HuggingFaceEndpoint(repo_id='tiiuae/falcon-7b-instruct', huggingfacehub_api_token=huggingfacehub_api_token)

# Predict the words following the text in question
question = 'Whatever you do, take care of your shoes'
output = llm.invoke(question)

print(output)

"""OpenAI models in LangChain!
OpenAI's models are particularly well-regarded in the AI/LLM community; their high performance is largely part to the use of their proprietary technology and carefully selected training data. In contrast to the open-source models on Hugging Face, OpenAI's models do have costs associated with their use.

Due to LangChain's unified syntax, swapping one model for another only requires changing a small amount of code. In this exercise, you'll do just that!

You do not need to create or provide an OpenAI API key for this course. The "<OPENAI_API_TOKEN>" placeholder will send valid requests to the API. If you encounter a RateLimitError, pause for a moment and try again."""

# Define the LLM
llm = OpenAI(model="gpt-3.5-turbo-instruct", api_key="<OPENAI_API_TOKEN>")

# Predict the words following the text in question
question = 'Whatever you do, take care of your shoes'
output = llm.invoke(question)

print(output)

"""Prompt templates and chaining
In this exercise, you'll begin using two of the core components in LangChain: prompt templates and chains!

Prompt templates are used for creating prompts in a more modular way, so they can be reused and built on. Chains act as the glue in LangChain; bringing the other components together into workflows that pass inputs and outputs between the different components.

The classes necessary for completing this exercise, including HuggingFaceEndpoint, have been pre-loaded for you."""

# Set your Hugging Face API token
huggingfacehub_api_token = '<HUGGING_FACE_TOKEN>'

# Create a prompt template from the template string
template = "You are an artificial intelligence assistant, answer the question. {question}"
prompt = PromptTemplate(template=template, input_variables=["question"])

# Create a chain to integrate the prompt template and LLM
llm = HuggingFaceEndpoint(repo_id='tiiuae/falcon-7b-instruct', huggingfacehub_api_token=huggingfacehub_api_token)
llm_chain = prompt | llm

question = "How does LangChain make LLM application development easier?"
print(llm_chain.invoke({"question": question}))

"""Chat prompt templates
Given the importance of chat models in many different LLM applications, LangChain provides functionality for accessing chat-specific models and chat prompt templates.

In this exercise, you'll define a chat model from OpenAI, and create a prompt template for it to begin sending it user input questions.

All of the LangChain classes necessary for completing this exercise have been pre-loaded for you."""

# Define an OpenAI chat model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key='<OPENAI_API_TOKEN>')		

# Create a chat prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "Respond to question: {question}")
    ]
)

# Chain the prompt template and model, and invoke the chain
llm_chain = prompt_template | llm
response = llm_chain.invoke({"question": "How can I retain learning?"})
print(response.content)

"""Integrating a chatbot message history
A key feature of chatbot applications is the ability to have a conversation, where context from the conversation history is stored and available for the model to access.

In this exercise, you'll create a conversation history that will be passed to the model. This history will contain every message in the conversation, including the user inputs and model responses.

All of the LangChain classes necessary for completing this exercise have been pre-loaded for you."""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key='<OPENAI_API_TOKEN>')

# Create the conversation history and add the first AI message
history = ChatMessageHistory()
history.add_ai_message("Hello! Ask me anything about Python programming!")

# Add the user message to the history
history.add_user_message("What is a list comprehension?")

# Add another user message and call the model
history.add_user_message("Describe the same in fewer words")
ai_response = llm.invoke(history.messages)
print(ai_response.content)

"""Creating a memory buffer
For many applications, storing and accessing the entire conversation history isn't technically feasible. In these cases, the messages must be condensed while retaining as much relevant context as possible. One common way of doing this is with a memory buffer, which stores only the most recent messages.

In this exercise, you'll integrate a memory buffer into an OpenAI chat model using an LCEL chain.

All of the LangChain classes necessary for completing this exercise have been pre-loaded for you."""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key='<OPENAI_API_TOKEN>')

# Define a buffer memory
memory = ConversationBufferMemory(size=4)

# Define the chain for integrating the memory with the model
buffer_chain = ConversationChain(llm=llm, memory=memory)

# Invoke the chain with the inputs provided
buffer_chain.invoke("Write Python code to draw a scatter plot.")
buffer_chain.invoke("Use the Seaborn library.")

"""Implementing a summary memory
For longer conversations, storing the entire memory, or even a long buffer memory, may not be technically feasible. In these cases, a summary memory implementation can be a good option. Summary memories summarize the conversation at each step to retain only the key context for the model to use. This works by using another LLM for generating the summaries, alongside the LLM used for generating the responses.

In this exercise, you'll implement a chatbot summary memory, using an OpenAI chat model for generating the summaries.

All of the LangChain classes necessary for completing this exercise have been pre-loaded for you."""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key='<OPENAI_API_TOKEN>')

# Define a summary memory that uses an OpenAI chat model
memory = ConversationSummaryMemory(llm=llm)

# Define the chain for integrating the memory with the model
summary_chain = ConversationChain(llm=llm, memory=memory, verbose=True)

# Invoke the chain with the inputs provided
summary_chain.invoke("Describe the relationship of the human mind with the keyboard when taking a great online class.")
summary_chain.invoke("Use an analogy to describe it.")


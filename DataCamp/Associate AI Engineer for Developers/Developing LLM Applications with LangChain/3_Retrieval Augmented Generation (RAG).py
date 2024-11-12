"""PDF document loaders
To begin implementing Retrieval Augmented Generation (RAG), you'll first need to load the documents that the model will access. These documents can come from a variety of sources, and LangChain supports document loaders for many of them.

In this exercise, you'll use a document loader to load a PDF document containing the paper, RAG VS Fine-Tuning: Pipelines, Tradeoffs, and a Case Study on Agriculture by Balaguer et al. (2024).

Note: pypdf, a dependency for loading PDF documents in LangChain, has already been installed for you."""

# Import library
from langchain_community.document_loaders import PyPDFLoader

# Create a document loader for rag_vs_fine_tuning.pdf
loader = PyPDFLoader('rag_vs_fine_tuning.pdf')

# Load the document
data = loader.load()
print(data[0])

"""CSV document loaders
Comma-separated value (CSV) files are an extremely common file format, particularly in data-related fields. Fortunately, LangChain provides different document loaders for different formats, keeping almost all of the syntax the same!

In this exercise, you'll use a document loader to load a CSV file containing data on FIFA World Cup international viewership. If your interested in the full analysis behind this data, check out How to Break FIFA."""

# Import library
from langchain_community.document_loaders.csv_loader import CSVLoader

# Create a document loader for fifa_countries_audience.csv
loader = CSVLoader('fifa_countries_audience.csv')

# Load the document
data = loader.load()
print(data[0])

"""HTML document loaders
It's possible to load documents from many different formats, including complex formats like HTML.

In this exercise, you'll load an HTML file containing a White House executive order."""

from langchain_community.document_loaders import UnstructuredHTMLLoader 

# Create a document loader for unstructured HTML
loader = UnstructuredHTMLLoader("white_house_executive_order_nov_2023.html")

# Load the document
data = loader.load()

# Print the first document
print(data[0])

# Print the first document's metadata
print(data[0].metadata)

"""Splitting by character
A key process in implementing Retrieval Augmented Generation (RAG) is splitting documents into chunks for storage in a vector database.

There are several splitting strategies available in LangChain, some with more complex routines than others. In this exercise, you'll implement a character text splitter, which splits documents based on characters and measures the chunk length by the number of characters.

Remember that there is no ideal splitting strategy, you may need to experiment with a few to find the right one for your use case."""

# Import the character splitter
from langchain_text_splitters import CharacterTextSplitter

quote = 'Words are flowing out like endless rain into a paper cup,\nthey slither while they pass,\nthey slip away across the universe.'
chunk_size = 24
chunk_overlap = 10

# Create an instance of the splitter class
splitter = CharacterTextSplitter(
    separator='\n',
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap)

# Split the string and print the chunks
docs = splitter.split_text(quote) 
print(docs)
print([len(doc) for doc in docs])

"""Recursively splitting by character
Many developers are using a recursive character splitter to split documents based on a specific list of characters. These characters are paragraphs, newlines, spaces, and empty strings, by default: ["\n\n", "\n", " ", ""].

Effectively, the splitter tries to split by paragraphs, checks to see if the chunk_size and chunk_overlap values are met, and if not, splits by sentences, then words, and individual characters.

Often, you'll need to experiment with different chunk_size and chunk_overlap values to find the ones that work well for your documents."""

# Import the recursive character splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

quote = 'Words are flowing out like endless rain into a paper cup,\nthey slither while they pass,\nthey slip away across the universe.'
chunk_size = 24
chunk_overlap = 10

# Create an instance of the splitter class
splitter = RecursiveCharacterTextSplitter(
    separators=["\n", " ", ""],
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap)

# Split the document and print the chunks
docs = splitter.split_text(quote) 
print(docs)
print([len(doc) for doc in docs])

"""Splitting HTML
In this exercise, you'll split an HTML containing an executive order on AI created by the US White House in October 2023. To retain as much context as possible in the chunks, you'll split using larger chunk_size and chunk_overlap values.

All of the LangChain classes necessary for completing this exercise have been pre-loaded for you."""

# Load the HTML document into memory
loader = UnstructuredHTMLLoader("white_house_executive_order_nov_2023.html")
data = loader.load()

# Define variables
chunk_size = 300
chunk_overlap = 100

# Split the HTML
splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    separators=['.'])

docs = splitter.split_documents(data) 
print(docs)

"""Preparing the documents and vector database
Over the next few exercises, you'll build a full RAG workflow to have a conversation with a PDF document containing the paper, RAG VS Fine-Tuning: Pipelines, Tradeoffs, and a Case Study on Agriculture by Balaguer et al. (2024). This works by splitting the documents into chunks, storing them in a vector database, defining a prompt to connect the retrieved documents and user input, and building a retrieval chain for the LLM to access this external data.

In this exercise, you'll prepare the document for storage and ingest them into a Chroma vector database. You'll use a RecursiveCharacterTextSplitter to chunk the PDF, and ingest them into a Chroma vector database using an OpenAI embeddings function. As with the rest of the course, you don't need to provide your own OpenAI API key.

The following classes have already been imported for you: RecursiveCharacterTextSplitter, Chroma, and OpenAIEmbeddings."""

loader = PyPDFLoader('rag_vs_fine_tuning.pdf')
data = loader.load()

# Split the document using RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50)
docs = splitter.split_documents(data) 

# Embed the documents in a persistent Chroma vector database
embedding_function = OpenAIEmbeddings(api_key='<OPENAI_API_TOKEN>', model='text-embedding-3-small')
vectorstore = Chroma.from_documents(
    docs,
    embedding=embedding_function,
    persist_directory=os.getcwd()
)

# Configure the vector store as a retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

"""Building a retrieval prompt template
Now your documents have been ingested into vector database and are ready for retrieval, you'll need to design a chat prompt template to combine the retrieved document chunks with the user input question.

The general structure of the prompt has already been provided; your goal is to insert the correct input variable placeholders into the message string and convert the string into a chat prompt template."""

# Add placeholders to the message string
message = """
Answer the following question using the context provided:

Context:
{context}

Question:
{question}

Answer:
"""

# Create a chat prompt template from the message string
prompt_template = ChatPromptTemplate.from_messages([("human", message)])

"""Creating a RAG chain
Now to bring all the components together in your RAG workflow! You've prepared the documents and ingested them into a Chroma database for retrieval. You created a prompt template to include the retrieved chunks from the academic paper and answer questions.

The prompt template you created in the previous exercise is available as prompt_template, an OpenAI model has been initialized as llm, and the code to recreate your retriever has be included in the script."""

vectorstore = Chroma.from_documents(
    docs,
    embedding=OpenAIEmbeddings(api_key='<OPENAI_API_TOKEN>', model='text-embedding-3-small'),
    persist_directory=os.getcwd()
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# Create a chain to link retriever, prompt_template, and llm
rag_chain = ({"context": retriever, "question": RunnablePassthrough()}
            | prompt_template
            | llm)

# Invoke the chain
response = rag_chain.invoke("Which popular LLMs were considered in the paper?")
print(response.content)


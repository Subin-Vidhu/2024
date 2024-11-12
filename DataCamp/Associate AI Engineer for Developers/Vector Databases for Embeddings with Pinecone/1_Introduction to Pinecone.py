"""Creating a Pinecone client
Throughout the course, you'll write Python code to interact with Pinecone via the Pinecone Python client. As a first step, you'll need to create your own Pinecone API key. Pinecone API keys used in this course's exercises will not be stored in any way.

To create a key, you'll first need to create a Pinecone starter account, which is free, by visiting https://www.pinecone.io/. Next, navigate to the API Keys page to create your key"""

# Import the Pinecone library
from pinecone import Pinecone

# Initialize the Pinecone client
pc = Pinecone(api_key="<PINECONE_TOKEN>")

"""Your first Pinecone index
With your Pinecone client initialized, you're all set to begin creating an index! Indexes are used to store records, including the vectors and associated metadata, as well as serving queries and other manipulations. As you progress through the course, you'll see how these different steps build up to a modern AI system built on a vector database.

If you accidentally create a valid index that doesn't meet the specifications detailed in the instructions, you'll need to add the following code before your .create_index() code to delete it and re-create it:

pc.delete_index('my-first-index')
The Pinecone class has already been imported for you."""

# Import ServerlessSpec
from pinecone import ServerlessSpec

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>") # Replace <PINECONE_TOKEN> with your Pinecone API key, created in the Pinecone dashboard

# Create your Pinecone index
pc.create_index(
    name="my-first-index", 
    dimension=256, 
    spec=ServerlessSpec(
        cloud='aws', 
        region='us-east-1'
    )
)

"""Connecting to an index
To begin ingesting vectors and performing vector manipulations in your newly-created Pinecone index, you'll first need to connect to it! The resulting index object has a number of methods for ingesting, manipulating, and exploring the contents of the index in Python.

The Pinecone class has already been imported for you, and will be available throughout the course."""


# Set up the client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

# Connect to your index
index = pc.Index("my-first-index")

# Print the index statistics
print(index.describe_index_stats())

"""Deleting an index
If you have an index that has gone stale, perhaps it's time to delete it! Deleting an index will also delete all of the data it contains, so be cautious when doing this in your own projects!"""

# Set up the client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

# Delete your Pinecone index
pc.delete_index("my-first-index")

# List your indexes
print(pc.list_indexes())

"""The Pinecone ecosystem
The Pinecone ecosystem consists of several different components, and you've learned about: organizations, projects, indexes, namespaces, and records. """

"""Checking dimensionality
You now have the know-how to begin ingesting vectors into a new Pinecone index! Before you jump in, you should check that your vectors are compatible with the dimensionality of your new index.

A list of dictionaries containing records to ingest has been provided as vectors. Here's a preview of its structure:

vectors = [
    {
        "id": "0",
        "values": [0.025525547564029694, ..., 0.0188823901116848]
        "metadata": {"genre": "action", "year": 2024}
    },
        ...,
]
If you accidentally create a valid index that doesn't meet the specifications detailed in the instructions, you'll need to add the following code before your .create_index() code:

pc.delete_index('datacamp-index')"""

# Initialize the Pinecone client using your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

# Create your Pinecone index
pc.create_index(
    name="datacamp-index", 
    dimension=1536, 
    spec=ServerlessSpec(
        cloud='aws', 
        region='us-east-1'
    )
)

# Check that each vector has a dimensionality of 1536
vector_dims = [len(vector['values']) == 1536 for vector in vectors]
print(all(vector_dims))

"""Ingesting vectors with metadata
It's ingesting time! You'll be ingesting vectors, which is a list of dictionaries containing the vector values, IDs, and associated metadata. They're already been provided in a format that can be directly inserted into the index without further manipulation.

Here's another reminder about the structure of vectors.

vectors = [
    {
        "id": "0",
        "values": [0.025525547564029694, ..., 0.0188823901116848]
        "metadata": {"genre": "action", "year": 2024}
    },
        ...,
]"""

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

# Connect to your index
index = pc.Index("datacamp-index")

# Ingest the vectors and metadata
index.upsert(
    vectors=vectors
)

# Print the index statistics
print(index.describe_index_stats())


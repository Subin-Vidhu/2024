"""Querying vs. fetching
In Pinecone, there are two primary methods for accessing vectors from an index: fetching and querying."""

"""Fetching vectors
In this exercise, you've been provided with a list of ids containing IDs of different records in your 'datacamp-index' index. You'll use these IDs to retrieve the associated records and explore their metadata."""

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

index = pc.Index('datacamp-index')
ids = ['2', '5', '8']

# Fetch vectors from the connected Pinecone index
fetched_vectors = index.fetch(ids=ids)

# Extract the metadata from each result in fetched_vectors
metadatas = [fetched_vectors['vectors'][id]['metadata'] for id in ids]
print(metadatas)
"""
Returning the most similar vectors
Querying vectors is foundational to so many AI applications. It involves embedding a user input, comparing it to the vectors in the database, and returning the most similar vectors.

In this exercise, you've been provided with a mystery vector called vector and you'll use it to query your index called 'datacamp-index'."""

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

index = pc.Index('datacamp-index')

# Retrieve the top three most similar records
query_result = index.query(
    vector=vector,
    top_k=3
)

print(query_result)

"""Changing distance metrics
By default, Pinecone indexes using the cosine similarity distance metric to compute similarity scores between vectors, which are used when querying to find the most similar vectors. Pinecone also supports other distance metrics, including Euclidean distance and the dot product.

The distance metric is set when the index is created, and can't be changed afterwards. In this exercise, you'll practice creating an index that uses the dot product distance metric."""

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

# Create an index that uses the dot product distance metric
pc.create_index(
    name="dotproduct-index",
    dimension=1536,
    metric='dotproduct',
    spec=ServerlessSpec(
        cloud='aws',
        region='us-east-1'
    )
)

# Print a list of your indexes
print(pc.list_indexes())

"""Filtering queries
In this exercise, you'll practice querying the 'datacamp-index' Pinecone index. You'll connect to the index and query it using the vector provided to retrieve similar vectors. You'll also use metadata filtering to optimize your querying and return the most relevant search results."""

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

index = pc.Index('datacamp-index')

# Retrieve the MOST similar vector with the year 2024
query_result = index.query(
    vector=vector,
    top_k=1,
    filter={
        "year": 2024
    }
)
print(query_result)

"""Multiple metadata filters
As well as equality operations, Pinecone provides operators for other core comparison operations, as well as enabling multiple filters in a single query. In this exercise, you'll create multiple filters using Pinecone's other comparison operators and use them to re-query your index."""

# Initialize the Pinecone client using your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

index = pc.Index('datacamp-index')

# Retrieve the MOST similar vector with genre and year filters
query_result = index.query(
    vector=vector,
    top_k=1,
    filter={
        "genre": "thriller",
        "year": {"$lt": 2018}
    }
)
print(query_result)

"""Updating vector values
In dynamic environments, data evolves rapidly, and being able to seamlessly integrate new values and metadata into existing vectors keeps your applications relevant and accurate.

In this exercise, you'll practice updating vectors in the 'datacamp-index' Pinecone index with new values. You'll verify these changes were successful by fetching the vector and checking its metadata."""

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

index = pc.Index('datacamp-index')

# Update the values of vector ID 7
index.update(
    id="7",
    values=vector
)

# Fetch vector ID 7
fetched_vector = index.fetch(ids=['7'])
print(fetched_vector)

"""Updating vector metadata
This time, you'll practice updating vectors in the datacamp-index Pinecone index with new metadata. You'll again verify these changes were successful by retrieving the vector and checking its metadata."""

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

index = pc.Index('datacamp-index')

# Update the metadata of vector ID 7
index.update(
    id="7",
    set_metadata={
        "genre": "thriller", 
        "year": 2024} 
)

# Fetch vector ID 7
fetched_vector = index.fetch(ids=['7'])
print(fetched_vector)
"""
Deleting vectors
Deleting vectors isn't just about tidying up our databases; it's about optimizing performance. As your indexes grow, unnecessary or outdated vectors can clutter your storage and slow down query performance. By removing redundant data, you streamline your operations, leading to faster responses and better resource utilization.

In this exercise, you'll practice deleting vectors from the 'datacamp-index' Pinecone index. You'll check the index metrics to verify the deletion took place.

If you accidentally delete the vectors but don't pass the exercise for a different reason, add the following code before your .delete() code to re-upsert the vectors for deletion:

index.upsert(vectors=vectors)"""

# Initialize the Pinecone client using your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

index = pc.Index('datacamp-index')

# Delete vectors
index.delete(
  ids=["3", "4"]
)

# Retrieve metrics of the connected Pinecone index
print(index.describe_index_stats())
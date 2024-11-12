"""Getting started with ChromaDB
In the following exercises, you'll use a vector database to embed and query 1000 films and TV shows from the Netflix dataset introduced in the video. The goal will be to use this data to generate recommendations based on a search query. To get started, you'll create the database and collection to store the data.

chromadb is available for you to use, and the OpenAIEmbeddingFunction() has been imported from chromadb.utils.embedding_functions. As with the first two chapters, you don't need to provide an OpenAI API key in this chapter."""

# Create a persistant client
client = chromadb.PersistentClient()

# Create a netflix_title collection using the OpenAI Embedding function
collection = client.create_collection(
    name="netflix_titles",
    embedding_function=OpenAIEmbeddingFunction(model_name="text-embedding-3-small", api_key="<OPENAI_API_TOKEN>")
)

# List the collections
print(client.list_collections())

"""Estimating embedding costs with tiktoken
Now that we've created a database and collection to store the Netflix films and TV shows, we can begin embedding data.

Before embedding a large dataset, it's important to do a cost estimate to ensure you don't go over any budget restraints. Because OpenAI models are priced by number of tokens inputted, we'll use OpenAI's tiktoken library to count the number of tokens and convert them into a dollar cost.

You've been provided with documents, which is a list containing all of the data to embed. You'll iterate over the list, encode each document, and count the total number of tokens. Finally, you'll use the model's pricing to convert this into a cost."""

# Load the encoder for the OpenAI text-embedding-3-small model
enc = tiktoken.encoding_for_model("text-embedding-3-small")

# Encode each text in documents and calculate the total tokens
total_tokens = sum(len(enc.encode(text)) for text in documents)

cost_per_1k_tokens = 0.00002

# Display number of tokens and cost
print('Total tokens:', total_tokens)
print('Cost:', cost_per_1k_tokens * total_tokens/1000)

"""Adding data to the collection
Time to add those Netflix films and TV shows to your collection! You've been provided with a list of document IDs and texts, stored in ids and documents, respectively, which have been extracted from netflix_titles.csv using the following code:

ids = []
documents = []

with open('netflix_titles.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for i, row in enumerate(reader):
    ids.append(row['show_id'])
    text = f"Title: {row['title']} ({row['type']})\nDescription: {row['description']}\nCategories: {row['listed_in']}"
    documents.append(text)
As an example of what information will be embedded, here's the first document from documents:

Title: Dick Johnson Is Dead (Movie)
Description: As her father nears the end of his life, filmmaker Kirsten Johnson stages his death in inventive and comical ways to help them both face the inevitable.
Categories: Documentaries
All of the necessary functions and packages have been imported, and a persistent client has been created and assigned to client."""

# Recreate the netflix_titles collection
collection = client.create_collection(
  name="netflix_titles",
  embedding_function=OpenAIEmbeddingFunction(model_name="text-embedding-3-small", api_key="<OPENAI_API_TOKEN>")
)

# Add the documents and IDs to the collection
collection.add(ids=ids, documents=documents)

# Print the collection size and first ten items
print(f"No. of documents: {collection.count()}")
print(f"First ten documents: {collection.peek()}")

"""Querying the Netflix collection
Now that you've created and populated the netflix_titles collection, it's time to query it!

As a first trial, you'll use it to provide recommendations for films and TV shows about dogs to one of your colleagues who loves dogs!

The netflix_titles collection is still available to use, and OpenAIEmbeddingFunction() has been imported."""

# Retrieve the netflix_titles collection
collection = client.get_collection(
  name="netflix_titles",
  embedding_function=OpenAIEmbeddingFunction(model_name="text-embedding-3-small", api_key="<OPENAI_API_TOKEN>")
)

# Query the collection for "films about dogs"
result = collection.query(
  query_texts=["films about dogs"],
  n_results=3
)

print(result)

"""Updating and deleting items from a collection
Just because the documents have been stored away in a vector database, that doesn't mean that you can't make changes to add to the collection or update existing items.

In this exercise, you've been provided with two new Netflix titles stored in new_data:

[{"id": "s1001", "document": "Title: Cats & Dogs (Movie)\nDescription: A look at the top-secret, high-tech espionage war going on between cats and dogs, of which their human owners are blissfully unaware."},
 {"id": "s6884", "document": 'Title: Goosebumps 2: Haunted Halloween (Movie)\nDescription: Three teens spend their Halloween trying to stop a magical book, which brings characters from the "Goosebumps" novels to life.\nCategories: Children & Family Movies, Comedies'}]
You'll either add or update these IDs in the database depending on whether they're already present in the collection."""

collection = client.get_collection(
  name="netflix_titles",
  embedding_function=OpenAIEmbeddingFunction(model_name="text-embedding-3-small", api_key="<OPENAI_API_TOKEN>")
)

# Update or add the new documents
collection.upsert(
    ids=[doc['id'] for doc in new_data],
    documents=[doc['document'] for doc in new_data]
)

# Delete the item with ID "s95" and re-run the query
collection.delete(ids=["s95"])

result = collection.query(
    query_texts=["films about dogs"],
    n_results=3
)
print(result)

"""Querying with multiple texts
In many cases, you'll want to query the vector database using multiple query texts. Recall that these query texts are embedded using the same embedding function as when the documents were added.

In this exercise, you'll use the documents from two IDs in the netflix_titles collection to query the rest of the collection, returning the most similar results as recommendations.

The netflix_titles collection is still available to use, and OpenAIEmbeddingFunction() has been imported."""

collection = client.get_collection(
  name="netflix_titles",
  embedding_function=OpenAIEmbeddingFunction(model_name="text-embedding-3-small", api_key="<OPENAI_API_TOKEN>")
)

reference_ids = ['s999', 's1000']

# Retrieve the documents for the reference_ids
reference_texts = collection.get(ids=reference_ids)['documents']

# Query using reference_texts
result = collection.query(
  query_texts=reference_texts,
  n_results=3
)

print(result['documents'])

"""Filtering using metadata
Having metadata available to use in the database can unlock the ability to more easily filter results based on additional conditions. Imagine that the film recommendations you've be creating could access the user's set preferences and use those to further filter the results.

In this exercise, you'll be using additional metadata to filter your Netflix film recommendations. The netflix_titles collection has been updated to add metadatas to each title, including the 'rating', the age rating given to the title, and 'release_year', the year the title was initially released.

Here's a preview of an updated item:

{'ids': ['s999'],
 'embeddings': None,
 'metadatas': [{'rating': 'TV-14', 'release_year': 2021}],
 'documents': ['Title: Searching For Sheela (Movie)\nDescription: Journalists and fans await Ma Anand Sheela as the infamous former Rajneesh commune’s spokesperson returns to India after decades for an interview tour.\nCategories: Documentaries, International Movies'],
 'uris': None,
 'data': None}"""

collection = client.get_collection(
  name="netflix_titles",
  embedding_function=OpenAIEmbeddingFunction(model_name="text-embedding-3-small", api_key="<OPENAI_API_TOKEN>")
)

reference_texts = ["children's story about a car", "lions"]

# Query two results using reference_texts
result = collection.query(
  query_texts=reference_texts,
  n_results=2,
  # Filter for titles with a G rating released before 2019
  where={
    "$and": [
        {"rating": 
        	{"$eq": "G"}
        },
        {"release_year": 
         	{"$lt": 2019}
        }
    ]
  }
)

print(result['documents'])


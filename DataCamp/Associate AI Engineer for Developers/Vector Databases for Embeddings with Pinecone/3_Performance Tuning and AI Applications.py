"""Defining a function for chunking
To be able to batch upserts in a reproducible way, you'll need to define a function to split your list of vectors into chunks.

The built-in itertools module has already been imported for you."""

def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    # Convert the iterable into an iterator
    it = iter(iterable)
    # Slice the iterator into chunks of size batch_size
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        # Yield the chunk
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

"""Batching upserts in chunks
In this exercise, you'll practice ingesting vectors into the 'datacamp-index' Pinecone index in series, batch-by-batch.

The chunks() helper function you created in the previous exercise is available to use:

def chunks(iterable, batch_size=100):
    "A helper function to break an iterable into chunks of size batch_size."
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))"""       

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

index = pc.Index('datacamp-index')

# Upsert vectors in batches of 100
for chunk in chunks(vectors):
    index.upsert(vectors=chunk) 

# Retrieve statistics of the connected Pinecone index
print(index.describe_index_stats())        

"""Batching upserts in parallel
In this exercise, you'll practice ingesting vectors into the 'datacamp-index' Pinecone index in parallel. You'll need to connect to the index, upsert vectors in batches asynchronously, and check the updated metrics of the 'datacamp-index' index.

The chunks() helper function you created earlier is still available to use:

def chunks(iterable, batch_size=100):
    "A helper function to break an iterable into chunks of size batch_size."
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))"""

# Initialize the client
pc = Pinecone(api_key="<PINECONE_TOKEN>", pool_threads=20)

index = pc.Index('datacamp-index')

# Upsert vectors in batches of 200 vectors
with pc.Index('datacamp-index', pool_threads=20) as index:
    async_results = [index.upsert(vectors=chunk, async_req=True) for chunk in chunks(vectors, batch_size=200)]
    [async_result.get() for async_result in async_results]

# Retrieve statistics of the connected Pinecone index
print(index.describe_index_stats())
"""
Namespaces
Namespaces are used to separate vectors within a single index, allowing targeted queries and minimizing the number of scanned records.

In this exercise, you'll practice ingesting vectors into different namespaces within the 'datacamp-index' Pinecone index. You'll need to connect to the index, upsert vectors into different namespaces, and check the updated metrics of the index."""

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

index = pc.Index('datacamp-index')

# Upsert vector_set1 to namespace1
index.upsert(
    vectors=vector_set1,
    namespace="namespace1"
)

# Upsert vector_set2 to namespace2
index.upsert(
    vectors=vector_set2,
    namespace="namespace2"
)

# Print the index statistics
index.describe_index_stats()

"""
Querying namespaces
Now that you've created separate namespaces and embraced multitenancy, it's time to reap the rewards! In this exercise, you'll query one of these new namespaces to search through only a segment of your full index."""

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

index = pc.Index('datacamp-index')

# Query namespace1 with the vector provided
query_result = index.query(
    vector=vector,
    namespace="namespace1",
    top_k=3
)
print(query_result)
"""
Creating and configuring a Pinecone index
To kickstart your semantic search application, you'll create and configure a new Pinecone index named 'pinecone-datacamp'. You'll use this in subsequent exercises to host Wikipedia articles from the SQuAD dataset.

If you accidentally create a valid index that doesn't meet the specifications detailed in the instructions, you'll need to add the following code before your .create_index() code:

pc.delete_index('pinecone-datacamp')"""

# Initialize the Pinecone client with your API key
pc = Pinecone(api_key="<PINECONE_TOKEN>")

# Create Pinecone index
pc.create_index(
    name='pinecone-datacamp', 
    dimension=1536,
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)

# Connect to index and print the index statistics
index = pc.Index('pinecone-datacamp')
print(index.describe_index_stats())

"""Upserting vectors for semantic search
Time to embed some text data and upsert the vectors and metadata into your 'pinecone-datacamp' index! You've be given a dataset named squad_dataset.csv, and a sample of 200 rows has been loaded in the DataFrame, df.

In this exercise, to interact with the OpenAI API to use their embedding model, you don't need to create and use your own API key. A valid OpenAI client has been created for you and assigned to the client variable.

Your task is to embed the text using OpenAI's API and upsert the embeddings and metadata into the Pinecone index under the namespace, squad_dataset."""

# Initialize the Pinecone client
pc = Pinecone(api_key="<PINECONE_TOKEN>")
index = pc.Index('pinecone-datacamp')

batch_limit = 100

for batch in np.array_split(df, len(df) / batch_limit):
    # Extract the metadata from each row
    metadatas = [{
      "text_id": row['id'],
      "text": row['text'],
      "title": row['title']} for _, row in batch.iterrows()]
    texts = batch['text'].tolist()
    
    ids = [str(uuid4()) for _ in range(len(texts))]
    
    # Encode texts using OpenAI
    response = client.embeddings.create(input=texts, model="text-embedding-3-small")
    embeds = [np.array(x.embedding) for x in response.data]
    
    # Upsert vectors to the correct namespace
    index.upsert(vectors=zip(ids, embeds, metadatas), namespace='squad_dataset')

"""Querying vectors for semantic search
In this exercise, you'll create a query vector from the question, 'What is in front of the Notre Dame Main Building?'. Using this embedded query, you'll query the 'squad_dataset' namespace from the 'pinecone-datacamp' index and return the top five most similar vectors."""    

# Initialize the Pinecone client
pc = Pinecone(api_key="<PINECONE_TOKEN>")
index = pc.Index('pinecone-datacamp')

query = "What is in front of the Notre Dame Main Building?"

# Create the query vector
query_response = client.embeddings.create(
    input=query,
    model="text-embedding-3-small"
)
query_emb = query_response.data[0].embedding

# Query the index and retrieve the top five most similar vectors
retrieved_docs = index.query(
    vector=query_emb,
    top_k=5,
    namespace="squad_dataset")

for result in retrieved_docs['matches']:
    print(f"{result['id']}: {round(result['score'], 2)}")
    print('\n')

"""Upserting YouTube transcripts
In this following exercises, you'll create a chatbot that can answer questions about YouTube videos by ingesting video transcripts and additional metadata into your 'pinecone-datacamp' index.

To start, you'll prepare data from the youtube_rag_data.csv file and upsert the vectors with all of their metadata into the 'pinecone-datacamp' index. The data is provided in the DataFrame youtube_df.

Here's an example transcript from the youtube_df DataFrame:

id: 
35Pdoyi6ZoQ-t0.0

title:
Training and Testing an Italian BERT - Transformers From Scratch #4

text: 
Hi, welcome to the video. So this is the fourth video in a Transformers from Scratch 
mini series. So if you haven't been following along, we've essentially covered what 
you can see on the screen. So we got some data. We built a tokenizer with it...

url: 
https://youtu.be/35Pdoyi6ZoQ

published: 
01-01-2024"""    

# Initialize the Pinecone client
pc = Pinecone(api_key="<PINECONE_TOKEN>")
index = pc.Index('pinecone-datacamp')

batch_limit = 100

for batch in np.array_split(youtube_df, len(youtube_df) / batch_limit):
    # Extract the metadata from each row
    metadatas = [{
      "text_id": row['id'],
      "text": row['text'],
      "title": row['title'],
      "url": row['url'],
      "published": row['published']} for _, row in batch.iterrows()]
    texts = batch['text'].tolist()
    
    ids = [str(uuid4()) for _ in range(len(texts))]
    
    # Encode texts using OpenAI
    response = client.embeddings.create(input=texts, model="text-embedding-3-small")
    embeds = [np.array(x.embedding) for x in response.data]
    
    # Upsert vectors to the correct namespace
    index.upsert(vectors=zip(ids, embeds, metadatas), namespace='youtube_rag_dataset')

print(index.describe_index_stats())
"""
Building a retrieval function
A key process in the Retrieval Augmented Generation (RAG) workflow is retrieving data from the database. In this exercise, you'll design a custom function called retrieve() that will perform this crucial process in the final exercise of the course."""

# Initialize the Pinecone client
pc = Pinecone(api_key="<PINECONE_TOKEN>")
index = pc.Index('pinecone-datacamp')

# Define a retrieve function that takes four arguments: query, top_k, namespace, and emb_model
def retrieve(query, top_k, namespace, emb_model):
    # Encode the input query using OpenAI
    query_response = client.embeddings.create(
        input=query,
        model=emb_model
    )
    
    query_emb = query_response.data[0].embedding
    
    # Query the index using the query_emb
    docs = index.query(vector=query_emb, top_k=top_k, namespace=namespace, include_metadata=True)
    
    retrieved_docs = []
    sources = []
    for doc in docs['matches']:
        retrieved_docs.append(doc['metadata']['text'])
        sources.append((doc['metadata']['title'], doc['metadata']['url']))
        
    return retrieved_docs, sources

documents, sources = retrieve(
  query="How to build next-level Q&A with OpenAI",
  top_k=3,
  namespace='youtube_rag_dataset',
  emb_model="text-embedding-3-small"
)
print(documents)
print(sources)

"""RAG questions answering function
You're almost there! The final piece in the RAG workflow is to integrate the retrieved documents with a question-answering model.

A prompt_with_context_builder() function has already been defined and made available to you. This function takes the documents retrieved from the Pinecone index, and integrates them into a prompt that the question-answering model can ingest:

def prompt_with_context_builder(query, docs):
    delim = '\n\n---\n\n'
    prompt_start = 'Answer the question based on the context below.\n\nContext:\n'
    prompt_end = f'\n\nQuestion: {query}\nAnswer:'

    prompt = prompt_start + delim.join(docs) + prompt_end
    return prompt
You'll implement the question_answering() function, which will provide OpenAI's language model gpt-4o-mini with additional context and sources with which it can answer your questions."""

# Initialize the Pinecone client
pc = Pinecone(api_key="<PINECONE_TOKEN>")
index = pc.Index('pinecone-datacamp')

query = "How to build next-level Q&A with OpenAI"

# Retrieve the top three most similar documents and their sources
documents, sources = retrieve(query, top_k=3, namespace='youtube_rag_dataset', emb_model="text-embedding-3-small")

prompt_with_context = prompt_with_context_builder(query, documents)
print(prompt_with_context)

def question_answering(prompt, sources, chat_model):
    sys_prompt = "You are a helpful assistant that always answers questions."
    
    # Use OpenAI chat completions to generate a response
    res = client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    answer = res.choices[0].message.content.strip()
    answer += "\n\nSources:"
    for source in sources:
        answer += "\n" + source[0] + ": " + source[1]
    
    return answer

answer = question_answering(
  prompt=prompt_with_context,
  sources=sources,
  chat_model='gpt-4o-mini')
print(answer)
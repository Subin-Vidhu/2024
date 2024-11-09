"""Embeddings applications
Embedding models convert text into numerical representations that are able to capture the context and intent behind the text. This unlocks powerful applications beyond what is possible with other types of AI models."""

"""Creating embeddings
In this exercise, you'll create your very first embeddings using the OpenAI API. Normally, to interact with the OpenAI API, you would need an OpenAI API key, and creating embeddings would incur a cost. However, you do not need to create or provide an API key in this course.

The <OPENAI_API_TOKEN> placeholder has been provided in the code, which will send valid requests for the exercises in this course. If, at any point in the course, you hit a RateLimitError, pause for a moment and try again."""

# Create an OpenAI client
client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a request to obtain embeddings
response = client.embeddings.create(
  model="text-embedding-3-small",
  input="This can contain any text."
)

# Convert the response into a dictionary
response_dict = response.model_dump()
print(response_dict)

"""Digging into the embeddings response
You've been able to successfully use the OpenAI Embeddings endpoint to embed text data, and in this exercise, you'll finish this off by extracting information from the API's response.

You've been provided with a response from the Embeddings API, which has already been converted into a dictionary and stored as response_dict. You'll need to extract the desired information from this dictionary. This response_dict has been printed for you, so you can view its contents and structure."""

# Extract the total_tokens from response_dict
print(response_dict['usage']['total_tokens'])

# Extract the embeddings from response_dict
print(response_dict['data'][0]['embedding'])

"""Embedding product descriptions
You've been provided with a list of dictionaries called products, which contains product information for different products sold by an online retailer. It's your job to embed the 'short_description' for each product to enable semantic search for the retailer's website.

Here's a preview of the products list of dictionaries:

products = [
    {
        "title": "Smartphone X1",
        "short_description": "The latest flagship smartphone with AI-powered features and 5G connectivity.",
        "price": 799.99,
        "category": "Electronics",
        "features": [
            "6.5-inch AMOLED display",
            "Quad-camera system with 48MP main sensor",
            "Face recognition and fingerprint sensor",
            "Fast wireless charging"
        ]
    },
    ...
]
An OpenAI client has already been created as assigned to client."""

# Extract a list of product short descriptions from products
product_descriptions = [product['short_description'] for product in products]

# Create embeddings for each product description
response = client.embeddings.create(
  model="text-embedding-3-small",
  input=product_descriptions
)
response_dict = response.model_dump()

# Extract the embeddings from response_dict and store in products
for i, product in enumerate(products):
    product['embedding'] = response_dict['data'][i]['embedding']
    
print(products[0].items())

"""Visualizing the embedded descriptions
Now that you've created embeddings from the product descriptions, it's time to explore them! You'll use t-SNE to reduce the number of dimensions in the embeddings data from 1,536 to two, which will make the data much easier to visualize.

You'll start with the products list of dictionaries you worked with in the last exercise, containing product information and the embeddings you created from the 'short_description'. As a reminder, here's a preview of products:

products = [
    {
        "title": "Smartphone X1",
        "short_description": "The latest flagship smartphone with AI-powered features and 5G connectivity.",
        "price": 799.99,
        "category": "Electronics",
        "features": [
            "6.5-inch AMOLED display",
            "Quad-camera system with 48MP main sensor",
            "Face recognition and fingerprint sensor",
            "Fast wireless charging"
        ],
        "embedding": [-0.014650369994342327, ..., 0.008677126839756966]
    },
    ...
]
matplotlib.pyplot and numpy have been imported as plt and np, respectively."""

# Create reviews and embeddings lists using list comprehensions
categories = [product['category'] for product in products]
embeddings = [product['embedding'] for product in products]

# Reduce the number of embeddings dimensions to two using t-SNE
tsne = TSNE(n_components=2, perplexity=5)
embeddings_2d = tsne.fit_transform(np.array(embeddings))

# Create a scatter plot from embeddings_2d
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])

for i, category in enumerate(categories):
    plt.annotate(category, (embeddings_2d[i, 0], embeddings_2d[i, 1]))

plt.show()

"""Computing cosine distances
To identify the most semantically similar texts, you need to apply a distance metric. A popular choice is the cosine distance.

In this exercise, you've been provided with four vectors: A, B, C, and D. It's your task to find out which vector is most similar to A using cosine distance.

Which vector is the most similar to A?

distance has already been imported from scipy.spatial."""

"""More repeatable embeddings
As you continue to work with embeddings, you'll find yourself making repeated calls to OpenAI's embedding model. To make these calls in a more repeatable and modular way, it would be better to define a custom function called create_embeddings() that would output embeddings for any number of text inputs. In this exercise, you'll do just that!"""

# Define a create_embeddings function
def create_embeddings(texts):
  response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
  )
  response_dict = response.model_dump()

  return [data['embedding'] for data in response_dict['data']]

# Embed short_description and print
print(create_embeddings(short_description)[0])

# Embed list_of_descriptions and print
print(create_embeddings(list_of_descriptions))

"""Finding the most similar product
Being able to compute similarity between embeddings is a key step within embeddings applications. In this exercise, you'll return to the products list of dictionaries that you worked with previously, which contains the embedded short descriptions you also created earlier.

You'll compare a piece of text to these embedded descriptions to identify the most similar description.

numpy has been imported as np, and distance is available from scipy.spatial. A create_embeddings() function has already been defined for you and is available to use for creating embeddings from a single input."""

# Embed the search text
search_text = "soap"
search_embedding = create_embeddings(search_text)[0]

distances = []
for product in products:
  # Compute the cosine distance for each product description
  dist = distance.cosine(search_embedding, product["embedding"])
  distances.append(dist)

# Find and print the most similar product short_description    
min_dist_ind = np.argmin(distances)
print(products[min_dist_ind]['short_description'])


"""Enriching embeddings
Previously, when you embedded product information, you were limited to only embedding the product 'short_description', which captured some, but not all of the relevant product information available. In this exercise, you'll embed 'title', 'short_description', 'category', and 'features' to capture much more information.

Here's a reminder of the products list of dictionaries:

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
When combining the features into a single string, it should have the following structure:

Title: <product title>
Description: <product description>
Category: <product category>
Features: <feature 1>; <feature 2>; <feature 3>; ..."""

# Define a function to combine the relevant features into a single string
def create_product_text(product):
  return f"""Title: {product['title']}
Description: {product['short_description']}
Category: {product['category']}
Features: {'; '.join(product['features'])}"""

# Combine the features for each product
product_texts = [create_product_text(product) for product in products]

# Create the embeddings from product_texts
product_embeddings = create_embeddings(product_texts)

"""Sorting by similarity
Now that you've embedded all of your features, the next step is to compute the similarities. In this exercise, you'll define a function called find_n_closest(), which computes the cosine distances between a query vector and a list of embeddings and returns the n smallest distances and their indexes.

In the next exercise, you'll use this function to enable your semantic product search application.

distance has been imported from scipy.spatial."""

def find_n_closest(query_vector, embeddings, n=3):
  distances = []
  for index, embedding in enumerate(embeddings):
    # Calculate the cosine distance between the query vector and embedding
    dist = distance.cosine(query_vector, embedding)
    # Append the distance and index to distances
    distances.append({"distance": dist, "index": index})
  # Sort distances by the distance key
  distances_sorted = sorted(distances, key=lambda x: x["distance"])
  # Return the first n elements in distances_sorted
  return distances_sorted[0:n]

""" Semantic search for products
Time to put your find_n_closest() function to use! You'll test out your semantic product search on a test query, computing a sorted list of the five most semantically similar products, based on the enriched data you gave the model.

Here's a reminder of the find_n_closest() function you created in the previous exercise:

def find_n_closest(query_vector, embeddings, n=3):
    distances = []
    for index, embedding in enumerate(embeddings):
        distance = spatial.distance.cosine(query_vector, embedding)
        distances.append({"distance": distance, "index": index})
    distances_sorted = sorted(distances, key=lambda x: x["distance"])
    return distances_sorted[0:n]
The create_embeddings() function you created earlier is also available. Recall that it takes some text, and returns a list of lists containing the embeddings for each text. The products dictionary and the product_embeddings you created previously have also been loaded."""

# Create the query vector from query_text
query_text = "computer"
query_vector = create_embeddings(query_text)[0]

# Find the five closest distances
hits = find_n_closest(query_vector, product_embeddings, n=5)

print(f'Search results for "{query_text}"')
for hit in hits:
  # Extract the product at each index in hits
  product = products[hit['index']]
  print(product["title"])

"""Product recommendation system
In this exercise, you'll make a recommendation system for an online retailer that sells a variety of products. This system recommends three similar products to users who visit a product page but don't purchase, based on the last product they visited.

You've been provided with a list of dictionaries of products available on the site,

products = [
    {
        "title": "Smartphone X1",
        "short_description": "The latest flagship smartphone with AI-powered features and 5G connectivity.",
        "price": 799.99,
        "category": "Electronics",
        "features": [
            "6.5-inch AMOLED display",
            ...
            "Fast wireless charging"
        ]
    },
    ...
]
and a dictionary for the last product the user visited, stored in last_product.

The following custom functions defined earlier in the course are also available for you to use:

create_embeddings(texts) → returns a list of embeddings for each text in texts.
create_product_text(product) → combines the product features into a single string for embedding.
find_n_closest(query_vector, embeddings, n=3) → returns the n closest distances and their indexes between the query_vector and embeddings, based on cosine distances."""

# Combine the features for last_product and each product in products
last_product_text = create_product_text(last_product)
product_texts = [create_product_text(product) for product in products]

# Embed last_product_text and product_texts
last_product_embeddings = create_embeddings(last_product_text)[0]
product_embeddings = create_embeddings(product_texts)

# Find the three smallest cosine distances and their indexes
hits = find_n_closest(last_product_embeddings, product_embeddings)

for hit in hits:
  product = products[hit['index']]
  print(product['title'])

"""Adding user history to the recommendation engine
For many recommendation cases, such as film or purchase recommendation, basing the next recommendation on one data point will be insufficient. In these cases, you'll need to embed all or some of the user's history for more accurate and relevant recommendations.

In this exercise, you'll extend your product recommendation system to consider all of the products the user has previously visited, which are stored in a list of dictionaries called user_history.

The following custom functions are available for you to use: create_embeddings(texts), create_product_text(product), and find_n_closest(query_vector, embeddings, n=3). numpy has also been imported as np."""  

# Prepare and embed the user_history, and calculate the mean embeddings
history_texts = [create_product_text(product) for product in user_history]
history_embeddings = create_embeddings(history_texts)
mean_history_embeddings = np.mean(history_embeddings, axis=0)

# Filter products to remove any in user_history
products_filtered = [product for product in products if product not in user_history]

# Combine product features and embed the resulting texts
product_texts = [create_product_text(product) for product in products_filtered]
product_embeddings = create_embeddings(product_texts)

hits = find_n_closest(mean_history_embeddings, product_embeddings)

for hit in hits:
  product = products_filtered[hit['index']]
  print(product['title'])


"""Embedding restaurant reviews
One common classification task that embeddings are great for is sentiment analysis. In this and the following exercises, you'll navigate through the workflow of performing sentiment analysis using embeddings.

You've been provided with a small sample of restaurant reviews, stored in reviews, and sentiment labels stored in sentiments:

sentiments = [{'label': 'Positive'},
              {'label': 'Neutral'},
              {'label': 'Negative'}]

reviews = ["The food was delicious!",
           "The service was a bit slow but the food was good",
           "The food was cold, really disappointing!"]
You'll use zero-shot classification to classify the sentiment of these reviews by embedding the reviews and class labels.

The create_embeddings() function you created previously is also available to use."""  

# Create a list of class descriptions from the sentiment labels
class_descriptions = [sentiment['label'] for sentiment in sentiments]

# Embed the class_descriptions and reviews
class_embeddings = create_embeddings(class_descriptions)
review_embeddings = create_embeddings(reviews)


"""Classifying review sentiment
Now that you've calculated the embeddings, it's time to compute the cosine distances and extract the most similar label.

You'll do this by defining a function called find_closest(), which can be used to compare the embeddings between one vector and multiple others, and return the nearest distance and its index. You'll then loop over the reviews and and use find_closest() to find the closest distance for each review, extracting the classified label using the index.

The class_embeddings and review_embeddings objects you created in the last exercise are available for you to use, as well as the reviews and sentiments."""

# Define a function to return the minimum distance and its index
def find_closest(query_vector, embeddings):
  distances = []
  for index, embedding in enumerate(embeddings):
    dist = distance.cosine(query_vector, embedding)
    distances.append({"distance": dist, "index": index})
  return min(distances, key=lambda x: x["distance"])

for index, review in enumerate(reviews):
  # Find the closest distance and its index using find_closest()
  closest = find_closest(review_embeddings[index], class_embeddings)
  # Subset sentiments using the index from closest
  label = sentiments[closest['index']]['label']
  print(f'"{review}" was classified as {label}')

"""Embedding more detailed descriptions
One of the last predicted labels didn't seem representative of the review; this was probably down to the lack of information being captured when we're only embedding the class labels. This time, descriptions of each class will be embedded instead, so the model better "understands" that you're classifying restaurant reviews.

The following objects are available for you to use:

sentiments = [{'label': 'Positive',
               'description': 'A positive restaurant review'},
              {'label': 'Neutral',
               'description':'A neutral restaurant review'},
              {'label': 'Negative',
               'description': 'A negative restaurant review'}]

reviews = ["The food was delicious!",
           "The service was a bit slow but the food was good",
           "The food was cold, really disappointing!"]"""  

# Extract and embed the descriptions from sentiments
class_descriptions = [sentiment['description'] for sentiment in sentiments]
class_embeddings = create_embeddings(class_descriptions)
review_embeddings = create_embeddings(reviews)

def find_closest(query_vector, embeddings):
  distances = []
  for index, embedding in enumerate(embeddings):
    dist = distance.cosine(query_vector, embedding)
    distances.append({"distance": dist, "index": index})
  return min(distances, key=lambda x: x["distance"])

for index, review in enumerate(reviews):
  closest = find_closest(review_embeddings[index], class_embeddings)
  label = sentiments[closest['index']]['label']
  print(f'"{review}" was classified as {label}')           

  
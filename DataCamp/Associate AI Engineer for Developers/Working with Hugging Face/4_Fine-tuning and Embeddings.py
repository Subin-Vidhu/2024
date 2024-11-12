"""Preparing a dataset
Fine-tuning a model requires several steps including identifying the model to fine-tune, preparing the dataset, creating the training loop object, then saving the model.

A model trained on English text classification has been identified for you, but it's up to you to prepare the imdb dataset in order to fine-tune this model to classify the sentiment of movie reviews.

The imdb dataset is already loaded for you and saved as dataset."""

# Import modules
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "distilbert-base-uncased-finetuned-sst-2-english"

# Load the model
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Use tokenizer on text
dataset = dataset.map(lambda row: tokenizer(row["text"], padding=True, max_length=512, truncation=True), keep_in_memory=True)

"""Building the trainer
To fine-tune a model, it must be trained on new data. This is the process of the model learning patterns within a training dataset, then evaluating how well it can predict patterns in an unseen test dataset. The goal is to help the model build an understanding of patterns while also being generalizable to new data yet to be seen.

Build a training object to fine-tune the "distilbert-base-uncased-finetuned-sst-2-english" model to be better at identifying sentiment of movie reviews.

The training_data and testing_data dataset are available for you. Trainer and TrainingArguments from transformers are also loaded. They were modified for the purpose of this exercise."""

# Create training arguments
training_args = TrainingArguments(output_dir="./results")

# Create the trainer
trainer = Trainer(
    model=model, 
    args=training_args, 
    train_dataset=training_data, 
    eval_dataset=testing_data
)

# Start the trainer
trainer.train()

"""Using the fine-tuned model
Now that the model is fine-tuned, it can be used within pipeline tasks, such as for sentiment analysis. At this point, the model is typically saved to a local directory (i.e. on your own computer), so a local file path is needed.

You'll use the newly fine-tuned distilbert model. There is a sentence, "I am a HUGE fan of romantic comedies.", saved as text_example.

Note: we are using our own pipeline module for this exercise for teaching purposes. The model is "saved" (i.e. not really) under the path ./fine_tuned_model."""

# Create the classifier
classifier = pipeline(task="sentiment-analysis", model="./fine_tuned_model")

# Classify the text
results = classifier(text=text_example)

print(results)

"""Generating text from a text prompt
Generating text can be accomplished using Auto classes from the Hugging Face transformers library. It can be a useful method for developing content, such as technical documentation or creative material.

You'll walk through the steps to process the text prompt, "Wear sunglasses when its sunny because", then generate new text from it.

AutoTokenizer and AutoModelForCausalLM from the transformers library are already loaded for you."""

# Set model name
model_name = "gpt2"

# Get the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

prompt = "Wear sunglasses when its sunny because"

# Tokenize the input
input_ids = tokenizer.encode(prompt, return_tensors="pt")

# Generate the text output
output = model.generate(input_ids, num_return_sequences=1)

# Decode the output
generated_text = tokenizer.decode(output[0])

print(generated_text)


"""Generating a caption for an image
Generating text can be done for modalities other than text, such as images. This has a lot of benefits including faster content creation by generating captions from images.

You'll create a caption for a fashion image using the Microsoft GIT model ("microsoft/git-base-coco").

AutoProcessor and AutoModelForCausalLM from the transformers library is already loaded for you along with the image."""

# Get the processor and model
processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")

# Process the image
pixels = processor(images=image, return_tensors="pt").pixel_values

# Generate the ids
output = model.generate(pixel_values=pixels)

# Decode the output
caption = processor.batch_decode(output)

print(caption[0])

"""Benefits and challenges of embeddings
Embeddings are a fantastic tool with benefits for many applications such as recommender systems, fraud detection, search, and more. However, even without their power for understanding patterns, there are also challenges."""

"""Generate embeddings for a sentence
Embeddings are playing an increasingly big role in ML and AI systems. A common use case is embedding text to support search.

The sentence-transformers package from Hugging Face is useful for getting started with embedding models. You'll compare the embedding shape from two different models - "all-MiniLM-L6-v2" and "sentence-transformers/paraphrase-albert-small-v2". This can determine which is better suited for a project (i.e. because of storage constraints).

The sentence used for embedding, "Programmers, do you put your comments (before|after) the related code?", is saved as sentence."""

# Create the first embedding model
embedder1 = SentenceTransformer("all-MiniLM-L6-v2")

# Embed the sentence
embedding1 = embedder1.encode([sentence])

# Create and use second embedding model
embedder2 = SentenceTransformer("sentence-transformers/paraphrase-albert-small-v2")
embedding2 = embedder2.encode([sentence])
 
# Compare the shapes
print(embedding1.shape == embedding2.shape)

# Print embedding1
print(embedding1)

"""Semantic search versus keyword search
Semantic search and keyword search are both technologies for returning relevant content based on a user query, or search. Each have their pros and cons which makes them suitable for different scenarios."""

"""Using semantic search
The similarity, or closeness, between a query and the other sentences, or documents, is the foundation for semantic search. This is a search method which takes into account context and intent of the query. Similarity measures, such as cosine similarity, are used to quantify the distance between the query and each sentence within the dimensional space. Results of a search are based on the closest sentences to the query.

You will use semantic search to return the top two Reddit threads relevant to the user query, "I need a desktop book reader for Mac"."""

query = "I need a desktop book reader for Mac"

# Generate embeddings
query_embedding = embedder.encode([query])[0]

# Compare embeddings
hits = util.semantic_search(query_embedding, sentence_embeddings, top_k=2)

# Print the top results
for hit in hits[0]:
    print(sentences[hit["corpus_id"]], "(Score: {:.4f})".format(hit["score"]))
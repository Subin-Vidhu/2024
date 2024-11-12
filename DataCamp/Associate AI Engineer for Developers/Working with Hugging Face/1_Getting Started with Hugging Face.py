"""Use cases for Hugging Face
Hugging Face is a versatile platform for machine learning and AI tasks. It hosts a plethora of community-sourced models, datasets, and solutions for common text, computer vision, and audio processing pipelines. Therefore, there are many benefits to using the Hugging Face ecosystem of tools and Python packages. However, there are some scenarios in which a different solution may be more appropriate."""

"""Searching the Hub with Python
The Hugging Face Hub provides a nice user interface for searching for models and learning more about them. At times, you may find it convenient to be able to do the same thing without leaving the development environment. Fortunately, Hugging Face also provides a Python package which allows you to find models through code.

Use the huggingface_hub package to find the most downloaded model for text classification.

HfApi and ModelFilter from the huggingface_hub package is already loaded for you."""

# Create the instance of the API
api = HfApi()

# Return the filtered list from the Hub
models = api.list_models(
    filter=ModelFilter(task="text-classification"),
    sort="downloads",
    direction=-1,
  	limit=1
)

# Store as a list
modelList = list(models)

print(modelList[0].modelId)

"""Saving a model
There may be situations where downloading and storing a model locally (i.e. a directory on your computer) is desired. For example, if working offline.

Practice downloading and saving here. An instance of AutoModel is already loaded for you under the same name."""

modelId = "distilbert-base-uncased-finetuned-sst-2-english"

# Instantiate the AutoModel class
model = AutoModel.from_pretrained(modelId)

# Save the model
model.save_pretrained(save_directory=f"models/{modelId}")
"""
Inspecting datasets
The datasets on Hugging Face range in terms of size, information, and features. Therefore it's beneficial to inspect it before committing to loading a dataset into your environment.

Let's inspect the "derenrich/wikidata-en-descriptions-small" dataset."""

# Load the module
from datasets import load_dataset_builder

# Create the dataset builder
reviews_builder = load_dataset_builder("derenrich/wikidata-en-descriptions-small")

# Print the features
print(reviews_builder.info.features)
"""
Loading datasets
Hugging Face built the dataset package for interacting with datasets. There are a lot of convenient functions, including load_dataset_builder which we just used. After inspecting a dataset to ensure its the right one for your project, it's time to load the dataset! For this, we can leverage input parameters for load_dataset to specify which parts of a dataset to load, i.e. the "train" dataset for English wikipedia articles.

The load_dataset module from the datasets package is already loaded for you. Note: the load_dataset function was modified for the purpose of this exercise."""

# Load the train portion of the dataset
wikipedia = load_dataset("wikimedia/wikipedia", language="20231101.en", split="train")

print(f"The length of the dataset is {len(wikipedia)}")

"""Manipulating datasets
There will likely be many occasions when you will need to manipulate a dataset before using it within a ML task. Two common manipulations are filtering and selecting (or slicing). Given the size of these datasets, Hugging Face leverages arrow file types.

This means performing manipulations are slightly different than what you might be used to. Fortunately, there's already methods to help with this!

The dataset is already loaded for you under wikipedia."""

# Filter the documents
filtered = wikipedia.filter(lambda row: "football" in row["text"])

# Create a sample dataset
example = filtered.select(range(1))

print(example[0]["text"])


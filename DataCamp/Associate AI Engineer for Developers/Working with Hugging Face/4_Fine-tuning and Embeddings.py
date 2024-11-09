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
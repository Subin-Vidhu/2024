"""Getting started with pipelines
Hugging Face has an ecosystem of libraries that allow users to leverage tools at different levels. The pipeline module from the transformers library is a great place to get started with performing ML tasks. It removes the requirement for training models, allowing for quicker experimentation and results. It does this by being a wrapper around underlying objects, functions, and processes.

Getting started with pipeline can be done by defining a task or model. This helps with quick experimentation as you become familiar with the library.

Create your first pipelines for sentiment analysis. The input is a sentence string that is already loaded for you."""

# Import pipeline
from transformers import pipeline

# Create the task pipeline
task_pipeline = pipeline(task="sentiment-analysis")

# Create the model pipeline
model_pipeline = pipeline(model="distilbert-base-uncased-finetuned-sst-2-english")

# Predict the sentiment
task_output = task_pipeline(input)
model_output = model_pipeline(input)

print(f"Sentiment from task_pipeline: {task_output[0]['label']}; Sentiment from model_pipeline: {model_output[0]['label']}")

"""Using AutoClasses
AutoClasses offer more control for machine learning tasks, and they can also be used with pipeline() for quick application. It's a nice balance of control and convenience.

Continue with the sentiment analysis task and combine AutoClasses with the pipeline module.

AutoModelForSequenceClassification and AutoTokenizer from the transformers library have already been imported for you and the input text is saved as input."""

# Download the model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# Create the pipeline
sentimentAnalysis = pipeline(task="sentiment-analysis", model=model, tokenizer=tokenizer)

# Predict the sentiment
output = sentimentAnalysis(input)

print(f"Sentiment using AutoClasses: {output[0]['label']}")

"""Comparing models with the pipeline
One of the great benefits of the pipeline() module is the ease at which you can experiment with different models simply by changing the "model" input. This is a good way to determine which model works best for a particular task or dataset that you are working with.

Experiment with two sentiment analysis models by creating pipelines for each, then using them to predict the sentiment for a sentence.

pipeline from the transformers library is already loaded for you. The example input sentence is saved as input."""

# Create the pipeline
distil_pipeline = pipeline(task="sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Predict the sentiment
distil_output = distil_pipeline(input)
"""
Comparing models with the pipeline
One of the great benefits of the pipeline() module is the ease at which you can experiment with different models simply by changing the "model" input. This is a good way to determine which model works best for a particular task or dataset that you are working with.

Experiment with two sentiment analysis models by creating pipelines for each, then using them to predict the sentiment for a sentence.

pipeline from the transformers library is already loaded for you. The example input sentence is saved as input."""

# Create the pipeline
distil_pipeline = pipeline(task="sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Predict the sentiment
distil_output = distil_pipeline(input)

# Create the second pipeline and predict the sentiment
bert_pipeline = pipeline(task="sentiment-analysis", model="kwang123/bert-sentiment-analysis")
bert_output = bert_pipeline(input)

print(f"Bert Output: {bert_output[0]['label']}")
print(f"Distil Output: {distil_output[0]['label']}")

"""Normalizing text
An important step to performing an NLP task is tokenizing the input text. This makes the text more understandable and manageable for the ML models, or other algorithms.

Before performing tokenization, it's best to run normalization steps, i.e. removing white spaces and accents, lowercasing, and more. Each tokenizer available in Hugging Face uses it's own normalization and tokenization processes.

Let's take a look at what normalization the distilbert-base-uncased tokenizer applies to the input_string, "HOWDY, how aré yoü?"."""

# Import the AutoTokenizer
from transformers import AutoTokenizer

# Download the tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Normalize the input string
output = tokenizer.backend_tokenizer.normalizer.normalize_str(input_string)

print(output)

"""Comparing tokenizer output
Most models in Hugging Face will have an associated tokenizer that will help prepare the input data based on what the model expects. After normalization, the tokenizer will split the input into smaller chunks based on the chosen algorithm. This is known as "pre-tokenization".

Let's explore the different types of pre-tokenization by performing this process with two tokenizers on the same input. We will be using DistilBertTokenizer and GPT2Tokenizer which have already been loaded for you. The input text string, "Pineapple on pizza is pretty good, I guess" is saved as input."""

# Download the gpt tokenizer
gpt_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Tokenize the input
gpt_tokens = gpt_tokenizer.tokenize(text=input)

# Repeat for distilbert
distil_tokenizer = DistilBertTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)
distil_tokens = distil_tokenizer.tokenize(text=input)

# Compare the output
print(f"GPT tokenizer: {gpt_tokens}")
print(f"DistilBERT tokenizer: {distil_tokens}")

"""Grammatical correctness
Text classification is the process of labeling an input text into a pre-defined category. This can take the form of sentiment - positive or negative - spam detection - spam or not spam - and even grammatical errors.

Explore the use of a text-classification pipeline for checking an input sentence for grammatical errors.

pipeline from the transformers library is already loaded for you."""

# Create a pipeline
classifier = pipeline(
    task="text-classification",
  model="abdulmatinomotoso/English_Grammar_Checker"
)

# Predict classification
output = classifier("I will walk dog")

print(output)

"""Question Natural Language Inference
Another task under the text classification umbrella is Question Natural Language Inference, or QNLI. This determines if a piece of text contains enough information to answer a posed question. This requires the model to perform logical reasoning which are important for Q&A applications.

Performing different tasks with the text-classification pipeline can be done by choosing different models. Each model is trained to predict specific labels and optimized for learning different context within a text.

pipeline from the transformers library is already loaded for you."""

# Create the pipeline
classifier = pipeline(task="text-classification", model="cross-encoder/qnli-electra-base")

# Predict the output
output = classifier("Where is the capital of France?, Brittany is known for their kouign-amann.")

print(output)

"""Zero-shot classification
Zero-shot classification is the ability for a transformer to predict a label from a new set of classes which it wasn't originally trained to identify. This is possible through its transfer learning capabilities. It can be an extremely valuable tool.

Hugging Face pipeline() also has a zero-shot-classification task. These pipelines require both an input text and candidate labels.

Build a zero-shot classifier to predict the label for the input text, a news headline that has been loaded for you.

pipelines from the transformers library is already loaded for you. Note that we are using our own version of the pipeline function to enable you to learn how to use these functions without having to download the model."""

# Build the zero-shot classifier
classifier = pipeline(task="zero-shot-classification", model="facebook/bart-large-mnli")

# Create the list
candidate_labels = ["politics", "science", "sports"]

# Predict the output
output = classifier(text, candidate_labels)

print(f"Top Label: {output['labels'][0]} with score: {output['scores'][0]}")

"""Summarizing long text
Summarization is a useful task for reducing large piece of text into something more manageable. This could be beneficial for multiple reasons like reducing the amount of time a reader needs to spend to obtain the important point of a piece of text.

The Hugging Face pipeline() task, "summarization", builds a s summarization pipeline which is a quick way to perform summarization on a piece of text. You'll do that by creating a new pipeline and using it to summarize a piece of text from a Wikipedia page on Greece."""

# Create the summarization pipeline
summarizer = pipeline(task="summarization", model="cnicu/t5-small-booksum")

# Summarize the text
summary_text = summarizer(original_text)

# Compare the length
print(f"Original text length: {len(original_text)}")
print(f"Summary length: {len(summary_text[0]['summary_text'])}")

"""Using min_length and max_length
The pipeline() function, has two important parameters: min_length and max_length. These are useful for adjusting the length of the resulting summary text to be short, longer, or within a certain number of words. You might want to do this if there are space constraints (i.e., small storage), to enhance readability, or improve the quality of the summary.

You'll experiment with a short and long summarizer by setting these two parameters to a small range, then a wider range."""

# Create a short summarizer
short_summarizer = pipeline(task="summarization", model="cnicu/t5-small-booksum", min_length=1, max_length=10)

# Summarize the input text
short_summary_text = short_summarizer(original_text)

# Print the short summary
print(short_summary_text[0]["summary_text"])

"""Using min_length and max_length
The pipeline() function, has two important parameters: min_length and max_length. These are useful for adjusting the length of the resulting summary text to be short, longer, or within a certain number of words. You might want to do this if there are space constraints (i.e., small storage), to enhance readability, or improve the quality of the summary.

You'll experiment with a short and long summarizer by setting these two parameters to a small range, then a wider range."""

# Create a short summarizer
short_summarizer = pipeline(task="summarization", model="cnicu/t5-small-booksum", min_length=1, max_length=10)

# Summarize the input text
short_summary_text = short_summarizer(original_text)

# Print the short summary
print(short_summary_text[0]["summary_text"])

# Repeat for a long summarizer
long_summarizer = pipeline(task="summarization", model="cnicu/t5-small-booksum", min_length=50, max_length=150)

long_summary_text = long_summarizer(original_text)

# Print the long summary
print(long_summary_text[0]["summary_text"])

"""Summarizing several inputs
Often times, you'll be working on projects where summarization will occur over an entire dataset or list of items, not just a single piece of text. Fortunately, this can be done by passing in a list of text items. This will return a list of summarized texts.

You'll build a final summarization pipeline and use it to summarize a list of text items from the wiki dataset."""

# Create the list
text_to_summarize = [w["text"] for w in wiki]

# Create the pipeline
summarizer = pipeline("summarization", model="cnicu/t5-small-booksum", min_length=20, max_length=50)

# Summarize each item in the list
summaries = summarizer(text_to_summarize[:3], truncation=True)

# Create for-loop to print each summary
for i in range(0,3):
  print(f"Summary {i+1}: {summaries[i]['summary_text']}")

  
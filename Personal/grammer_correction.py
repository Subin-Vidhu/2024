# pip install textblob, if not installed
from textblob import TextBlob

def grammer_correction(text):
    blob = TextBlob(text)
    return str(blob.correct())

while True:
    text = input("Enter text: ")
    print(f"Corrected text: {grammer_correction(text)}")
    if text == 'exit':
        break


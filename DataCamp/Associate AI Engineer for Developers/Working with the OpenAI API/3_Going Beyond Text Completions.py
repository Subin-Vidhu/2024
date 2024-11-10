"""Why use text moderation models?
Text moderation is a vital component of most social media platforms, internet chatrooms, and many other user-facing systems. It serves the purpose of preventing the distribution and promotion of inappropriate content, such as hate speech."""
"""
Requesting moderation
Aside from text and chat completion models, OpenAI provides models with other capabilities, including text moderation. OpenAI's text moderation model is designed for evaluating prompts and responses to determine if they violate OpenAI's usage policies, including inciting hate speech and promoting violence.

In this exercise, you'll test out OpenAI's moderation functionality on a sentence that may have been flagged as containing violent content using traditional word detection algorithms."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Create a request to the Moderation endpoint
response = client.moderations.create(
    model="text-moderation-latest",
    input="My favorite book is To Kill a Mockingbird."
)

print(response.results[0].category_scores)
"""
Creating a podcast transcript
The OpenAI API Audio endpoint provides access to the Whisper model, which can be used for speech-to-text transcription and translation. In this exercise, you'll create a transcript from a DataFramed podcast episode with OpenAI Developer, Logan Kilpatrick.

If you'd like to hear more from Logan, check out the full ChatGPT and the OpenAI Developer Ecosystem podcast episode."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Open the openai-audio.mp3 file
audio_file = open("openai-audio.mp3", "rb")

# Create a transcript from the audio file
response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

# Extract and print the transcript text
print(response.text)
"""
Transcribing a non-English language
The Whisper model can not only transcribe English language, but also performs well on speech in many other languages.

In this exercise, you’ll create a transcript from audio.m4a, which contains speech in Portuguese."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Open the audio.m4a file
audio_file= open("audio.m4a", "rb")

# Create a transcript from the audio file
response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

print(response.text)

"""Translating Portuguese
Whisper can not only transcribe audio into its native language but also supports translation capabilities for creating English transcriptions.

In this exercise, you'll return to the Portuguese audio, but this time, you'll translate it into English!"""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Open the audio.m4a file
audio_file = open("audio.m4a", "rb")

# Create a translation from the audio file
response = client.audio.translations.create(model="whisper-1", file=audio_file)

# Extract and print the translated text
print(response.text)
"""
Translating with prompts
The quality of Whisper's translation can vary depending on the language spoken, the audio quality, and the model's awareness of the subject matter. If you have any extra context about what is being spoken about, you can send it along with the audio to the model to give it a helping hand.

You've been provided with with an audio file, audio.wav; you're not sure what language is spoken in it, but you do know it relates to a recent World Bank report. Because you don't know how well the model will perform on this unknown language, you opt to send the model this extra context to steer it in the right direction."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Open the audio.wav file
audio_file = open("audio.wav", "rb")

# Write an appropriate prompt to help the model
prompt = "The transcript contains a discussion on a recent World Bank Report."

# Create a translation from the audio file
response = client.audio.translations.create(model="whisper-1",
                                            file=audio_file,
                                            prompt=prompt)

print(response.text)
"""
Identifying audio language
You've learned that you're not only limited to creating a single request, and that you can actually feed the output of one model as an input to another! This is called chaining, and it opens to the doors to more complex, multi-modal use cases.

In this exercise, you'll practice model chaining to identify the language used in an audio file. You'll do this by bringing together OpenAI's audio transcription functionality and its text models with only a few lines of code"""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Open the audio.wav file
audio_file = open("audio.wav", "rb")

# Create a transcription request using audio_file
audio_response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

# Create a request to the API to identify the language spoken
chat_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a languages specialist."},
        {"role": "user", "content": "Identify the language used in the following text: " + audio_response.text}
    ]
)
print(chat_response.choices[0].message.content)
"""
Creating meeting summaries
Time for business! One time-consuming task that many find themselves doing day-to-day is taking meeting notes to summarize attendees, discussion points, next steps, etc.

In this exercise, you'll use AI to augment this task to not only save a substantial amount of time, but also to empower attendees to focus on the discussion rather than administrative tasks. You've been provided with a recording from DataCamp's Q2 Roadmap webinar, which summarizes what DataCamp will be releasing during that quarter. You'll chain the Whisper model with a text or chat model to discover which courses will be launched in Q2."""

client = OpenAI(api_key="<OPENAI_API_TOKEN>")

# Open the datacamp-q2-roadmap.mp3 file
audio_file = open("datacamp-q2-roadmap.mp3", "rb")

# Create a transcription request using audio_file
audio_response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

# Create a request to the API to summarize the transcript into bullet points
chat_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "List the courses that DataCamp will be making as bullet points." + audio_response.text}
    ],
    max_tokens=100
)
print(chat_response.choices[0].message.content)


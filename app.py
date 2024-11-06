import streamlit as st
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
from io import BytesIO
import speech_recognition as sr
from transformers import pipeline
import tempfile

# Initialize Hugging Face pipeline for summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def record_audio(duration=30, sample_rate=16000):
    st.write("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait until recording is finished
    st.write("Recording finished.")
    return audio_data

def save_audio_file(audio_data, sample_rate):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav.write(f.name, sample_rate, audio_data)
        return f.name

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

def summarize_text(text):
    # Limit text to 1024 tokens for summarization model
    max_input_length = 1024
    input_text = text[:max_input_length] if len(text) > max_input_length else text
    summary = summarizer(input_text, max_length=100, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

# Streamlit UI
st.title("Meeting Minutes Generator (No FFmpeg)")

# Option to upload audio file
uploaded_file = st.file_uploader("Upload an audio file", type=["wav"])

# Option to record audio
if st.button("Record from Microphone"):
    audio_duration = st.slider("Select recording duration (seconds)", min_value=10, max_value=60, value=30)
    sample_rate = 16000
    audio_data = record_audio(duration=audio_duration, sample_rate=sample_rate)
    file_path = save_audio_file(audio_data, sample_rate)
    st.success("Audio recorded successfully.")
    transcript = transcribe_audio(file_path)
    st.write("### Transcription")
    st.write(transcript)
    
    if st.button("Generate Meeting Minutes"):
        summary = summarize_text(transcript)
        st.write("### Meeting Minutes")
        st.write(summary)

# Transcription from uploaded file
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(uploaded_file.read())
        file_path = f.name
    transcript = transcribe_audio(file_path)
    st.write("### Transcription")
    st.write(transcript)
    
    if st.button("Generate Meeting Minutes from File"):
        summary = summarize_text(transcript)
        st.write("### Meeting Minutes")
        st.write(summary)
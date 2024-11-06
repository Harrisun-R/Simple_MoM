import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import os
import wave

st.title("Minutes of Meeting Generator")

# Function to transcribe audio
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            transcription = recognizer.recognize_google(audio)
            return transcription
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Option to upload audio file
st.header("Upload your audio file")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    # Save the uploaded file to disk
    with open("temp_audio_file", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Convert the file to wav format if necessary
    if uploaded_file.type == "audio/mp3":
        audio = AudioSegment.from_mp3("temp_audio_file")
        audio.export("temp_audio_file.wav", format="wav")
        audio_file = "temp_audio_file.wav"
    else:
        audio_file = "temp_audio_file"

    # Transcribe the audio file
    transcription = transcribe_audio(audio_file)
    st.header("Transcription")
    st.write(transcription)

    # Generate Minutes of Meeting
    st.header("Minutes of the Meeting")
    lines = transcription.split('.')
    for i, line in enumerate(lines):
        st.write(f"{i + 1}. {line.strip()}")

    # Clean up the temporary files
    os.remove("temp_audio_file")
    if uploaded_file.type == "audio/mp3":
        os.remove("temp_audio_file.wav")

# Option to record audio from microphone
st.header("Record audio from your microphone")
if st.button("Start Recording"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Recording... Please speak clearly into the microphone.")
        audio = recognizer.listen(source)
        st.write("Recording complete.")

    # Save the recorded audio to a wav file
    with open("microphone_audio.wav", "wb") as f:
        f.write(audio.get_wav_data())

    # Transcribe the recorded audio
    transcription = transcribe_audio("microphone_audio.wav")
    st.header("Transcription")
    st.write(transcription)

    # Generate Minutes of Meeting
    st.header("Minutes of the Meeting")
    lines = transcription.split('.')
    for i, line in enumerate(lines):
        st.write(f"{i + 1}. {line.strip()}")

    # Clean up the temporary file
    os.remove("microphone_audio.wav")

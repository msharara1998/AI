import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import asyncio
from copy import deepcopy
from pathlib import Path
from send_email import send_email
import streamlit.components.v1 as components
from io import BytesIO
import os
import numpy as np

# Control variables
PH = "Speak or upload a file to display the corresponding transcription"

parent_dir = os.path.dirname(os.path.abspath(__file__))
# Custom REACT-based component for recording client audio in browser
build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
# specify directory and initialize st_audiorec object functionality
st_audiorec = components.declare_component("st_audiorec", path=build_dir)
# Session state
if "text" not in st.session_state:
    st.session_state["text"] = ""
    st.session_state["run"] = False

if "lang" not in st.session_state:
    st.session_state["lang"] = "ar-LB"



def extract_text_fromfile():
    if st.session_state["uploaded_file"] is None:
        st.warning("Please upload a file first")
    else:
        uploaded_file = st.session_state["uploaded_file"]

        if Path(uploaded_file.name).suffix != ".wav":
            sound = AudioSegment.from_file(uploaded_file)
            uploaded_file = sound.export(format="wav")

        src = sr.AudioFile(uploaded_file)
        r = sr.Recognizer()
        with src as source:
            audio = r.record(source)
        val = r.recognize_google(audio, language=st.session_state["lang"])
        st.session_state["text"] = val


def playfile():
    if uploaded_file is None:
        st.warning("Please upload a file first")
    else:
        if uploaded_file.name[len(uploaded_file.name) - 3 :] == "mp4":
            playvideo(deepcopy(uploaded_file))
        else:
            playaudio(deepcopy(uploaded_file))


def playaudio(audio):
    audio_bytes = audio.read()
    st.audio(audio_bytes, format="audio/ogg")


def playvideo(video):
    video_bytes = video.read()
    st.video(video_bytes)


def start_listening():
    st.session_state["run"] = True
    recorder.recording = True
    st.session_state["text"] = ""


def stop_listening():
    st.session_state["run"] = False
    recorder.recording = False
    recorder.save("test.wav")


def clear_text():
    st.session_state["text"] = ""


async def live_recognize():
    with sr.Microphone() as source:
        rec = sr.Recognizer()
        rec.adjust_for_ambient_noise(source, duration=0.5)
        while st.session_state["run"]:
            st.markdown("Listening...")
            audio = rec.listen(source, phrase_time_limit=10)
            try:
                # TODO try await
                result = rec.recognize_google(audio, language=st.session_state["lang"])
                st.session_state["text"] += result + "\n"

            except sr.UnknownValueError:
                st.markdown("Could not understand audio")
            except sr.RequestError as e:
                st.markdown(
                    "Could not request results from speech recognition service; {0}".format(
                        e
                    )
                )


# Constructing page
st.set_page_config(page_title='Speech Recognizer',page_icon='🎙️')
st.markdown("<h1 style='text-align: center; color: black;'>Speech Recognizer</h1>", unsafe_allow_html=True)
st.info('This application can transcribe live audio or a video/audio file you upload.', icon="ℹ️")

LANG = st.selectbox("Please Select a Language", options=["ar-LB", "en-US",'fr-FR'])
st.session_state["lang"] = LANG if LANG else "ar-LB"

tab1, tab2 = st.tabs(["Live", "Recorded"])
with tab1:
    val = st_audiorec()
    if isinstance(val, dict):  # retrieve audio data
        with st.spinner('Extracting Text data'):
            ind, val = zip(*val['arr'].items())
            ind = np.array(ind, dtype=int)  # convert to np array
            val = np.array(val)             # convert to np array
            sorted_ints = val[ind]
            stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
            wav_bytes = stream.read()
            with open("test.wav", "wb") as f:
                f.write(wav_bytes)
            src = sr.AudioFile("test.wav")
            r = sr.Recognizer()
            with src as source:
                audio = r.record(source)
            returned_text = r.recognize_google(audio, language=st.session_state["lang"])
            st.session_state["text"] = returned_text

with tab2:
    uploaded_file = st.file_uploader("Choose a file", type=["wav", "mp3", "mp4", "ogg"])
    if uploaded_file is not None:
        bytes_data=uploaded_file.get_value()
    st.session_state["uploaded_file"] = uploaded_file
    button_columns_tab2 = st.columns([1, 1])
    if button_columns_tab2[0].button("Play Uploaded File"):
        playfile()
    button_columns_tab2[1].button("Extract Text", on_click=extract_text_fromfile)


st.text_area("Transcription", st.session_state["text"], placeholder=PH)
if st.session_state['text']:
    st.success("Done!", icon="✅")
output_options = st.columns([1, 1, 1])
output_options[0].download_button(
    label="Download text",
    data=st.session_state["text"],
    file_name="transcribed_text.txt",
)
output_options[1].button("Send Email", on_click=send_email)
output_options[2].button("Clear text", on_click=clear_text)


if not st.session_state["run"] and st.session_state["text"]:
    if st.session_state["lang"] in ["en-US","fr-FR"]:
        st.session_state["text"] = (
            st.session_state["text"][0].upper() + st.session_state["text"][1:-1] + "."
        )
    else:
        st.session_state["text"] = st.session_state["text"] + "."
# asyncio.run(live_recognize())

from ast import Delete
from distutils.command.upload import upload
from turtle import onclick
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import winsound
# import asyncio
from functions import send_email

# Initializing page elements

title = st.container()
input = st.container()
language = st.container()
mode = st.container()
tab1, tab2 = st.tabs(['Live', 'Recorded'])
button_container = st.container()
button_columns = st.columns([1,1])
output = st.container()
output_options = st.columns([1,1,1])
txt=''

# Control variables
PH = 'Speak or upload a file to display the corresponding transcription'
# Session state
if 'text' not in st.session_state:
    st.session_state['text'] = ''
    st.session_state['run'] = False

if 'lang' not in st.session_state:
    st.session_state['lang'] = 'ar-LB'

# Defining necessary functions


# def start_listening():
#     st.session_state['run'] = True
#     st.session_state['text'] = 'Listening...'
def extract_text_fromfile():
    if uploaded_file is None:
        st.warning('Please upload a file first')
    else:
        if uploaded_file.name[len(uploaded_file.name) -3:] == 'mp3':
            sound = AudioSegment.from_mp3(uploaded_file)
            uploaded_file = sound.export('test.wav',format="wav")
            # with open('myfile.wav', mode="bw") as f:
            #     f.write(uploaded_file.getbuffer)

        # if uploaded_file.name[len(uploaded_file.name) -3:]=='mp4':
        #     #src
        src=sr.AudioFile(uploaded_file)
        r=sr.Recognizer()
        with src as source:
            audio=r.record(source)
        val=r.recognize_google(audio)
        st.session_state['text'] = val
        

def playfile():
    if uploaded_file is None:
        st.warning('Please upload a file first') 
    else:
        if uploaded_file.name[len(uploaded_file.name) -3:]=='mp4':
            playvideo(uploaded_file)
        else:
            playaudio(uploaded_file)

def playaudio(audio):
        audio_bytes = audio.read()
        with mode:
            st.audio(audio_bytes, format='audio/ogg')

def playvideo(video):
        video_bytes = video.read()
        with mode:
            st.video(video_bytes)


def stop_listening():
    st.session_state['run'] = False

def clear_text():
    st.session_state['text'] = uploaded_file
    winsound.PlaySound(uploaded_file, winsound. SND_FILENAME)

def recognize():
    st.session_state['run'] = True
    st.session_state['text'] = 'Listening...'
    while st.session_state['run']:
        rec = sr.Recognizer()
        # Function to convert speech to text
        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source, duration=0.5)
            audio = rec.listen(source)
            lang = st.session_state['lang']
            try:
                txt = rec.recognize_google(audio, language=lang)
                st.session_state['text'] = txt
            except sr.UnknownValueError:
                txt = "Google Speech Recognition could not understand audio"
                st.session_state['text'] = txt
            except sr.RequestError as e:
                txt = "Could not request results from Google Speech Recognition service; {0}".format(e)
                st.session_state['text'] = txt

# Constructing page
st.title('Speech Recognizer')
with input:
    with language:
        LANG = st.selectbox('Please Select a Language', options=['ar-LB', 'en-US'])
        st.session_state['lang'] = LANG
    with mode:
        with tab1:
            with button_columns[0]:
                if tab1:
                    st.button('Start', on_click=recognize)
            with button_columns[1]:
                st.button('Stop', on_click=stop_listening)
        with tab2:
            uploaded_file = st.file_uploader("Choose a file",type=["wav","mp3","mp4","ogg"])
            x = st.columns([1,1])
            with x[0]:
                if tab2:
                    st.button('Play Uploaded File',on_click=playfile)
            with x[1]:
                st.button('Extract Text',on_click= extract_text_fromfile)
with output:
    st.text_area('Transcription', st.session_state['text'], placeholder=PH)

    with output_options[0]:
        st.download_button(
            label='Download text',
            data=st.session_state['text'],
            file_name='transcribed_text.txt')
    with output_options[1]:
        email = st.button('Send Email')
    with output_options[2]:
        st.button('Clear text', on_click=clear_text)



# asyncio.run(recognize())

# A session is started whenever an instance of Streamlit app is
# opened in a browser. Each session exists as long as the tab is
# opened. Opening 2 tabs will create two independent sessions.
# A session is what happens in the browser and the state is how
# we store the current values of widgets and parameters to use
# later.



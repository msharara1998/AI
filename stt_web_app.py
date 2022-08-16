import streamlit as st
import speech_recognition as sr
import asyncio
from send_email import send_email

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

# Control variables
PH = 'Speak or upload a file to display the corresponding transcription'
#st.session_state
# Session state
if 'text' not in st.session_state:
    st.session_state['text'] = 'Listening...'
    st.session_state['run'] = False

if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en-US'


# Defining necessary functions
def start_listening():
    st.session_state['run'] = True
    #st.session_state['text'] = 'Listening...'
    #st.session_state['text'] = recognize()

def stop_listening():
    st.session_state['run'] = False


def clear_text():
    st.session_state['text'] = ''


async def recognize():
    # Function to convert speech to text
    with sr.Microphone() as source:

        rec = sr.Recognizer()
        rec.adjust_for_ambient_noise(source, duration=0.5)
        while st.session_state['run']:
            audio = rec.listen(source)
            lang = st.session_state['lang']
            try:
                st.session_state['text'] = rec.recognize_google(audio, language=lang)
                st.markdown(st.session_state['text'])
            except sr.UnknownValueError:
                return "Google Speech Recognition could not understand audio"

            except sr.RequestError as e:
                return "Could not request results from Google Speech Recognition service; {0}".format(e)


# Constructing page
with title:
    st.title('Speech Recognizer')
with input:
    with language:
        LANG = st.selectbox('Please Select a Language', options=['ar-LB', 'en-US'])
        st.session_state['lang'] = LANG
    with mode:
        with tab1:
            with button_columns[0]:
                st.button('Start', on_click=start_listening)
            with button_columns[1]:
                st.button('Stop', on_click=stop_listening)
        with tab2:
            uploaded_file = st.file_uploader("Choose a file")
with output:
    st.text_area('Transcription', st.session_state['text'], placeholder=PH)
    if st.session_state['text'] != '' and st.session_state['text'] != 'Listening...':
        with output_options[0]:
            st.download_button(
                label='Download text',
                data=st.session_state['text'],
                file_name='transcribed_text.txt')
        with output_options[1]:
            email = st.button('Send Email')
        with output_options[2]:
            st.button('Clear text', on_click=clear_text)


st.session_state
#asyncio.run(func())





import speech_recognition as sr
import asyncio
import time
from send_email import *

if "text" not in st.session_state:
    st.session_state["text"] = ""
    st.session_state["run"] = False


def start_listening():
    st.session_state["run"] = True
    st.session_state["text"] = ""


def stop_listening():
    st.session_state["run"] = False


def output_options():
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download text",
            data=st.session_state["text"],
            file_name="transcribed_text.txt",
        )
    with col2:
        st.button("Send Email", on_click=send_email)


def file_recognizer(audio_video_file):
    flag = False
    st.session_state["text"] = ""
    r = sr.Recognizer()
    audio_video_file = sr.AudioFile(audio_video_file)
    with audio_video_file as source:
        audio = r.record(source)
        try:
            with st.spinner("Wait for it..."):
                # time.sleep(2)
                result = r.recognize_google(audio, language=language)

            if language == "en-US":
                result = result[0].upper() + result[1:] + "."
            else:
                result = result + "."

            st.session_state["text"] = result
            st.text_area(label="Transcription:", value=result)
            st.success("Done!", icon="✅")
            flag = True
        except sr.UnknownValueError:
            st.markdown("Could not understand audio")
        except sr.RequestError as e:
            st.markdown(
                "Could not request results from speech recognition service; {0}".format(
                    e
                )
            )
    if flag:
        output_options()


st.title("Speech Recognizer")
language = st.selectbox("Choose language", ["ar-LB", "en-US"])
start, stop = st.columns(2)
start.button("Start listening", on_click=start_listening)
stop.button("Stop listening", on_click=stop_listening)
file = st.file_uploader(
    "Upload a .wav or a video file to output the corresponding transcription"
)
if file:
    file_recognizer(file)


async def live_recognize():
    with sr.Microphone() as source:
        rec = sr.Recognizer()
        rec.adjust_for_ambient_noise(source, duration=0.5)
        while st.session_state["run"]:
            st.markdown("Listening...")
            audio = rec.listen(source, phrase_time_limit=10)
            try:
                result = rec.recognize_google(audio, language=language)
                st.session_state["text"] += result + "\n"

            except sr.UnknownValueError:
                st.markdown("Could not understand audio")
            except sr.RequestError as e:
                st.markdown(
                    "Could not request results from speech recognition service; {0}".format(
                        e
                    )
                )


if not st.session_state["run"] and st.session_state["text"]:
    if language == "en-US":
        st.session_state["text"] = (
            st.session_state["text"][0].upper() + st.session_state["text"][1:-1] + "."
        )
    else:
        st.session_state["text"] = st.session_state["text"] + "."
    st.text_area(label="Transcription", value=st.session_state["text"])
    output_options()
asyncio.run(live_recognize())

# st.session_state

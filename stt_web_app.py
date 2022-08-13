import streamlit as st

# Referencing Style Sheet
with open('stt_web_app_style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initializing page elements
page = st.container()
header = st.container()
input = st.container()
language = st.container()
mode = st.container()
tab1, tab2 = st.tabs(['live', 'recorded'])
button_container = st.container()
button_columns = st.columns([3.8,1,3.8])
output = st.container()
output_options = st.columns([1,1,1,1])
ph = 'Speak or upload a file to display the corresponding transcription'
text = ''
# Constructing Page
with page:
    with header:
        st.markdown('''
<div id = 'title_wrapper'>
    <h1 style='text-align: center; color: black;'>Speech Recognizer</h1>
</div>
    ''', unsafe_allow_html=True)
    with input:
        with language:
            lang = None
            lang = st.selectbox('Please Select a Language', options=['Arabic', 'English'])
        with mode:
            with tab1:
                st.button('start')
            with tab2:
                uploaded_file = st.file_uploader("Choose a file")

    with output:
        txt = st.text_area('Transcription', text, placeholder=ph)
        with output_options[1]:
            st.download_button('Download text', text)
        with output_options[2]:
            st.button('send email')




#<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
#<div class = "input">
#<i class="fa-solid fa-microphone fa-4x"></i>
#<i class="fa fa-folder fa-4x" aria-hidden="true"></i>

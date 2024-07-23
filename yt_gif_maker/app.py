import streamlit as st
from yt_gif_maker.transcribe import avaliable_models
from yt_gif_maker.transcribe import transcribe
from yt_gif_maker.audio_extractor import extract_audio
from yt_gif_maker.create import bleep_replace
from yt_gif_maker.yt_download import download_video
import tempfile
import uuid
import io

app_name = "YouTube gif maker"
st.set_page_config(page_title=app_name)
st.title(app_name)

tab1, tab2 = st.tabs([app_name, "💡 About"])

with tab2:
    st.markdown(
        "### Make a gif of a one liner from any a YouTube video.  \n"
        "How it works: \n\n"
        "1.  Provided a youtube / shorts url \n"
        "2.  Enter in the phrase you want to gif-afy \n"
        "3.  (if running locally) Choose a model from the Whisper family to transcribe the audio (defaults to base only for HF space) \n"
        "4.  (optional) Press 'just transcribe' to examine / download just the transcription of the video (can help in choosing bleep words) \n"
        "5.  Press 'transcribe & clip' to transcribe and recover clips relevant to your input phrase \n"
        "6.  Click the 'gif-this' button next to the clip you want to gif-afy \n"
        "If you want to select your Whisper model / run longer videos pull and run the app locally. \n\n"
        "You do *not* need a GPU to run this locally.  Larger models take more time to process locally, but its doable. \n"
    )

with tab1:
    with st.container(border=True):
        upload_url = st.text_input(
            label="youtube url",
            value="https://www.youtube.com/watch?v=9m_12SGXNKw",
        )

    with st.container(border=True):
        col1, col2, col3 = st.columns([8, 3, 4])
        with col1:
            bleep_words = st.text_area(
                label="input phrase",
                placeholder="enter in the input phrase you'd like gif-a-fied",
                value="say hello to my little friend",
            )
        with col2:
            model_selection = st.selectbox(
                label="whisper model (base only in HF space)",
                index=1,
                options=avaliable_models,
            )
        with col3:
            col4 = st.empty()
            with col4:
                st.write("")
                st.write("")
            col5 = st.container()
            with col5:
                trans_button_val = st.button(label="just transcribe", type="secondary")
            col6 = st.container()
            with col6:
                clip_button_val = st.button(label="transcribe & clip", type="primary")

    a, col0, b = st.columns([1, 20, 1])
    colo1, colo2 = st.columns([3, 3])

    def button_logic(
        temporary_video_location: str,
        model_selection: str,
        phrase: list,
        upload_url: str,
    ):

        if trans_button_val:
            download_video(upload_url, temporary_video_location)
            filename = open(temporary_video_location, "rb")
            byte_file = io.BytesIO(filename.read())
            with open(temporary_video_location, "wb") as out:
                out.write(byte_file.read())
                with st.container(border=True):
                    with colo1:
                        st.caption("original video")
                        st.video(temporary_video_location)
                out.close()

            transcript, timestamped_words  = transcribe(video_file_path=temporary_video_location, model=model_selection)

            with col0.container(border=True):
                st.text_area(
                    value=transcript.strip(),
                    placeholder="transcribe text will be shown here",
                    label="transcribe text",
                )

        if clip_button_val:
            download_video(upload_url, temporary_video_location)
            filename = open(temporary_video_location, "rb")
            byte_file = io.BytesIO(filename.read())
            with open(temporary_video_location, "wb") as out:
                out.write(byte_file.read())
                with st.container(border=True):
                    with colo1:
                        st.caption("original video")
                        st.video(temporary_video_location)
                out.close()

            transcript, timestamped_words  = transcribe(video_file_path=temporary_video_location, model=model_selection)

            with col0.container(border=True):
                st.text_area(
                    value=transcript.strip(),
                    placeholder="transcribe text will be shown here",
                    label="transcribe text",
                )



    with tempfile.TemporaryDirectory() as tmpdirname:
        temporary_video_location = tmpdirname + "/original_" + str(uuid.uuid4()) + ".mp4"
        bleep_word_list = bleep_words.split(",")
        bleep_words_list = [v.strip() for v in bleep_word_list if len(v.strip()) > 0]
        button_logic(temporary_video_location, model_selection, bleep_words_list, upload_url)
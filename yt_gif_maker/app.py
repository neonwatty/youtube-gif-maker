import streamlit as st
from yt_gif_maker.transcribe import avaliable_models
from yt_gif_maker.transcribe import transcribe
from yt_gif_maker.yt_download import download_video
from yt_gif_maker.yt_transcript import get_single_transcript
from yt_gif_maker.nearest import get_nearest_snippets
from yt_gif_maker.gif_maker import clip_video_and_gif, draw_on_gif
import base64
import tempfile
import uuid
import io


# Initialization
if "yt_transcript_text" not in st.session_state:
    st.session_state.yt_transcript_text = ""
if "yt_just_transcript_text" not in st.session_state:
    st.session_state.yt_just_transcript_text = ""
if "temporary_video_location" not in st.session_state:
    st.session_state.temporary_video_location = ""
if "upload_url" not in st.session_state:
    st.session_state.upload_url = "https://www.youtube.com/shorts/43BhDHYBG0o"


def fetch_logic(upload_url: str, temporary_video_location: str):
    if yt_fetch_button:
        download_video(upload_url, temporary_video_location)
        filename = open(temporary_video_location, "rb")
        byte_file = io.BytesIO(filename.read())
        with open(temporary_video_location, "wb") as out:
            out.write(byte_file.read())
            with col_orig_video:
                with st.container(border=True):
                    st.caption("original video")
                    st.video(temporary_video_location)
                out.close()
        yt_transcript = get_single_transcript(upload_url)

        st.session_state.yt_transcript_text = yt_transcript

        all_text = yt_transcript["transcript"]
        all_text = " ".join([v["text"] for v in all_text])

        st.session_state.yt_just_transcript_text = all_text


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
        upload_url = st.text_input(label="YouTube / Shorts url", value=st.session_state.upload_url)
        yt_fetch_button = st.button(
            label="fetch video", type="secondary", on_click=fetch_logic, args=(st.session_state.upload_url, st.session_state.temporary_video_location)
        )

    with st.container(border=True):
        col_yt_trans, col_yt_whisper = st.columns([4, 4])
        with col_yt_trans.container(border=True):
            yt_trans_text_area = st.text_area(
                value=st.session_state.yt_just_transcript_text,
                placeholder="YouTube transcript will appear here if it exists",
                label="YouTube's transcript",
            )

        with col_yt_whisper.container(border=True):
            yt_whisper_text_area = st.text_area(
                value="",
                placeholder="Whisper transcript will appear here if you create it",
                label="Whisper transcript",
            )

    with st.container(border=True):
        col1, col2, col3 = st.columns([8, 3, 4])
        with col1:
            input_phrase = st.text_area(
                label="input phrase",
                placeholder="enter in the input phrase you'd like gif-a-fied",
                value="every time we'd mention costa rica",
            )
        with col2:
            model_selection = st.selectbox(
                label="whisper model (base only in HF space)",
                index=0,
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
    col_empty_1, col_orig_video, col_empty_2 = st.columns([4, 8, 4])

    def button_logic(
        temporary_video_location: str,
        model_selection: str,
        input_phrase: list,
        upload_url: str,
    ):
        if trans_button_val:
            download_video(upload_url, temporary_video_location)
            filename = open(temporary_video_location, "rb")
            byte_file = io.BytesIO(filename.read())
            with open(temporary_video_location, "wb") as out:
                out.write(byte_file.read())
                with col_orig_video:
                    with st.container(border=True):
                        st.caption("original video")
                        st.video(temporary_video_location)
                    out.close()

            transcript, timestamped_words = transcribe(video_file_path=temporary_video_location, model=model_selection)

            with col0.container(border=True):
                st.text_area(
                    value=transcript.strip(),
                    placeholder="transcribe text will be shown here",
                    label="transcribe text",
                )

        if clip_button_val:
            transcript, timestamped_words = transcribe(video_file_path=temporary_video_location, model=model_selection)
            closest_time_ranges = get_nearest_snippets(input_phrase, transcript, timestamped_words)

            output_clip_path = temporary_video_location[:-4] + "_clip_1.mp4"
            output_gif_path = temporary_video_location[:-4] + "_clip_1.gif"
            start_ms = closest_time_ranges[0][0]
            end_ms = closest_time_ranges[0][1]
            clip_video_and_gif(temporary_video_location, output_clip_path, output_gif_path, start_ms, end_ms)

            with col0.container(border=True):
                st.text_area(
                    value=transcript.strip(),
                    placeholder="transcribe text will be shown here",
                    label="transcribe text",
                )

            c00, c01, c02 = st.columns([8, 8, 8])
            filename = open(output_clip_path, "rb")
            byte_file = io.BytesIO(filename.read())
            with open(output_clip_path, "wb") as out:
                out.write(byte_file.read())
                with c00:
                    with st.container(border=True):
                        st.caption("clip 1 video")
                        st.video(output_clip_path)
                    out.close()

            filename = open(output_gif_path, "rb")
            byte_file = io.BytesIO(filename.read())
            with open(temporary_video_location, "wb") as out:
                out.write(byte_file.read())
                with c01:
                    with st.container(border=True):
                        st.caption("clip 1 gif")
                        st.image(output_gif_path)
                    out.close()

                    with open(output_gif_path, "rb") as file:
                        st.download_button(label="Download gif", data=file, file_name="clip_1.gif", mime="image/gif")

                        # file_ = open(output_gif_path, "rb")
                        # contents = file_.read()
                        # data_url = base64.b64encode(contents).decode("utf-8")
                        # file_.close()
                        # st.markdown(
                        #     f'<img src="data:image/gif;base64,{data_url}" alt="clip 1 gif">',
                        #     unsafe_allow_html=True,
                        # )

                    out.close()

    with tempfile.TemporaryDirectory() as tmpdirname:
        st.session_state.temporary_video_location = tmpdirname + "/original_" + str(uuid.uuid4()) + ".mp4"

        # button_logic(temporary_video_location, model_selection, input_phrase, upload_url)

import streamlit as st
from yt_gif_maker.transcribe import avaliable_models
from yt_gif_maker.transcribe import transcribe
from yt_gif_maker.yt_download import download_video
from yt_gif_maker.yt_transcript import get_single_transcript
from yt_gif_maker.nearest import get_nearest_snippets
from yt_gif_maker.gif_maker import clip_video_and_gif, draw_on_gif
from yt_gif_maker.clip import clip_video
import base64
import tempfile
import uuid
import io


# Initialization
if "yt_transcript_words" not in st.session_state:
    st.session_state.yt_transcript_words = None
if "yt_just_transcript" not in st.session_state:
    st.session_state.yt_just_transcript = None
if "whisper_transcript_words" not in st.session_state:
    st.session_state.whisper_transcript_words = None
if "whisper_just_transcript" not in st.session_state:
    st.session_state.whisper_just_transcript = None
if "temporary_video_location" not in st.session_state:
    with tempfile.TemporaryDirectory() as tmpdirname:
        st.session_state.temporary_video_location = tmpdirname + "/original_" + str(uuid.uuid4()) + ".mp4"
    
if "upload_url" not in st.session_state:
    st.session_state.upload_url = "https://www.youtube.com/shorts/43BhDHYBG0o"
if "input_phrase" not in st.session_state:
    if st.session_state.upload_url == "https://www.youtube.com/shorts/43BhDHYBG0o":
        st.session_state.input_phrase = "every time we'd mention costa rica"
    else:
        st.session_state.input_phrase = ""
if "model_selection" not in st.session_state:
    st.session_state.model_selection = "base"
if "model_selection_index" not in st.session_state:
    st.session_state.model_selection_index = 1


def clip_temp_videos(temporary_video_path: str, input_phrase: str) -> None:
    transcript = st.session_state.yt_just_transcript
    timestamped_words = st.session_state.yt_transcript_words
    if timestamped_words is None:
        return
    
    if st.session_state.whisper_transcript_words is not None:
        transcript = st.session_state.whisper_just_transcript
        timestamped_words = st.session_state.whisper_transcript_words

    closest_time_ranges, closest_chunks = get_nearest_snippets(input_phrase, transcript, timestamped_words) 
    
    clip_video_path = "/".join(temporary_video_path.split("/")[:-2]) + f"/test_clip_{str(0)}.mp4"
    start_ms = closest_time_ranges[0][0]
    end_ms = closest_time_ranges[0][1]
    recovered_phrase = closest_chunks[0]
    clip_video(temporary_video_path, clip_video_path, start_ms, end_ms)
    
    with st.container(border=True):
        filename = open(clip_video_path, "rb")
        byte_file = io.BytesIO(filename.read())
        with open(clip_video_path, "wb") as out:
            out.write(byte_file.read())
            with col_clip_1:
                with st.container(border=True):
                    st.caption(f"clip {str(0)}")
                    st.video(clip_video_path)
                out.close()

                col_recovered_phrase, col_gif_button = st.columns([4, 4])
                with col_recovered_phrase:
                    st.session_state.recovered_phrase_1 = recovered_phrase
                    st.text_area(label="similar phrase", value=st.session_state.recovered_phrase_1)


def fetch_logic(upload_url: str, temporary_video_location: str):
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

    transcript_text = yt_transcript["transcript"]
    transcript_words = yt_transcript["transcript_words"]

    st.session_state.yt_just_transcript = transcript_text
    st.session_state.yt_transcript_words = transcript_words


def transcribe_logic(
    temporary_video_location: str,
    model_selection: str,
):
    st.session_state.whisper_just_transcript, st.session_state.whisper_transcript_words = transcribe(video_file_path=temporary_video_location, model=model_selection)


app_name = "YouTube gif maker (advanced)"
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
        with st.container(border=True):
            st.markdown("## upload area")
            upload_url = st.text_input(label="YouTube / Shorts url", value=st.session_state.upload_url)
            yt_fetch_button = st.button(
                label="fetch video", type="secondary", on_click=fetch_logic, args=(st.session_state.upload_url, st.session_state.temporary_video_location)
            )

        col_video_empty_1, col_orig_video, col_video_empty_2 = st.columns([4, 8, 4])

    with st.container(border=True):
        st.markdown("## transcript area")
        col_yt_trans, col_yt_whisper = st.columns([4, 4])
        with col_yt_trans.container(border=True):
            yt_trans_text_area = st.text_area(
                value=st.session_state.yt_just_transcript,
                placeholder="YouTube transcript will appear here if it exists",
                label="YouTube's transcript",
            )

        with col_yt_whisper.container(border=True):
            yt_whisper_text_area = st.text_area(
                value=st.session_state.whisper_just_transcript,
                placeholder="Whisper transcript will appear here if you make it",
                label="Whisper transcript",
            )

            st.session_state.model_selection = st.selectbox(
                label="whisper model (base only in HF space)",
                index=st.session_state.model_selection_index,
                options=avaliable_models,
            )

            trans_button_val = st.button(label="transcribe with whisper", type="secondary", on_click=transcribe_logic, args=(st.session_state.temporary_video_location, st.session_state.model_selection))

    with st.container(border=True):
        st.markdown("## clip / gif maker area")
        input_phrase = st.text_input(
            label="input phrase",
            placeholder="enter in the input phrase you'd like gif-a-fied",
            value=st.session_state.input_phrase,
        )
        clip_button_val = st.button(label="phrase-clip", type="secondary",  on_click=clip_temp_videos, args=(st.session_state.temporary_video_location, st.session_state.input_phrase))
        
        col_clip_1, col_clip_recovered_phrase_1_2 = st.columns([4, 4])
        col_clip_empty_2_1, col_clip_2, col_clip_recovered_phrase_2_2 = st.columns([2, 8, 4])
        col_clip_empty_3_1, col_clip_3, col_clip_recovered_phrase_2_3 = st.columns([2, 8, 4])



#     a, col0, b = st.columns([1, 20, 1])
#     colo1, colo2 = st.columns([3, 3])

# st.session_state.input_phrase, st.session_state.transcript
# input_phrase
#                      transcript: str,
#                      timestamped_words: list,
#                      temporary_video_path: str,
#                      max_clips: int = 3)
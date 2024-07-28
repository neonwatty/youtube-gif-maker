import streamlit as st
import os
from yt_gif_maker.transcribe import transcribe
from yt_gif_maker.yt_download import download_video
from yt_gif_maker.yt_transcript import get_single_transcript
from yt_gif_maker.nearest import get_nearest_snippets
from yt_gif_maker.gif_maker import make_gif
from yt_gif_maker.clip import clip_video
from yt_gif_maker.streamlit_funcs.state import reset_state
from yt_gif_maker.config import default_temp_video_location


def clip_and_gif(before_phrase_secs: float, after_phrase_secs: float, resize_factor: float, fps: int, num_clips: int = 1) -> None:
    st.session_state.before_phrase_secs = before_phrase_secs
    st.session_state.after_phrase_secs = after_phrase_secs
    st.session_state.resize_factor = resize_factor
    st.session_state.fps = int(fps)

    transcript = st.session_state.yt_just_transcript
    timestamped_words = st.session_state.yt_transcript_words
    if timestamped_words is None:
        return

    if st.session_state.whisper_transcript_words is not None:
        transcript = st.session_state.whisper_just_transcript
        timestamped_words = st.session_state.whisper_transcript_words
        
    for i in range(num_clips):
        closest_time_ranges, closest_chunks = get_nearest_snippets(st.session_state.input_phrase, transcript, timestamped_words)

        clip_video_path = "/".join(st.session_state.temporary_video_path.split("/")[:-2]) + f"/test_clip_{str(i+1)}.mp4"
        clip_file_path_components = clip_video_path.split("/")
        clip_gif_path = "/".join(clip_file_path_components[:-2]) + "/" + clip_file_path_components[-1].split(".")[0] + ".gif"

        start_ms = closest_time_ranges[i][0]
        end_ms = closest_time_ranges[i][1]
        recovered_phrase = closest_chunks[i]

        st.session_state.recovered_phrases[i] = recovered_phrase
        st.session_state.clip_video_paths[i] = clip_video_path
        st.session_state.clip_gif_paths[i] = clip_gif_path

        clip_video(st.session_state.temporary_video_path, clip_video_path, start_ms, end_ms, st.session_state.before_phrase_secs, st.session_state.after_phrase_secs)
        make_gif(
            clip_video_path,
            clip_gif_path,
            st.session_state.input_phrase,
            st.session_state.text_on_gif_val,
            st.session_state.resize_factor,
            st.session_state.fps,
        )

        st.session_state.gif_sizes[i] = round(os.path.getsize(clip_gif_path) / (1024 * 1024), 2)


def fetch_logic(upload_url: str):
    if upload_url != st.session_state.upload_url:
        st.session_state.upload_url = upload_url
        reset_state(upload_url)
    st.session_state.temporary_video_location = default_temp_video_location()
    download_video(upload_url, st.session_state.temporary_video_location)
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
    st.session_state.whisper_just_transcript, st.session_state.whisper_transcript_words = transcribe(
        video_file_path=temporary_video_location, model=model_selection
    )


def auto_usage(upload_url: str, before_phrase_secs: float, after_phrase_secs: float, resize_factor: float, fps: int) -> None:
    fetch_logic(upload_url)
    clip_and_gif(before_phrase_secs, after_phrase_secs, resize_factor, fps, 1)
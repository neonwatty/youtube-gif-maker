import streamlit as st
from yt_gif_maker.config import (
    default_yt_transcript_words,
    default_yt_just_transcript,
    default_whisper_transcript_words,
    default_whisper_just_transcript,
    default_upload_url,
    default_input_phrase,
    default_whisper_model_selection,
    default_whisper_model_selection_index,
    default_clip_video_path,
    default_clip_gif_path,
    default_recovered_phrase,
    default_gif_size,
    default_text_on_gif_val,
    default_before_phrase_secs,
    default_after_phrase_secs,
    default_resize_factor,
    default_fps,
    default_temp_video_location,
)


def init_state():
    if "yt_transcript_words" not in st.session_state:
        st.session_state.yt_transcript_words = default_yt_transcript_words
    if "yt_just_transcript" not in st.session_state:
        st.session_state.yt_just_transcript = default_yt_just_transcript
    if "whisper_transcript_words" not in st.session_state:
        st.session_state.whisper_transcript_words = default_whisper_transcript_words
    if "whisper_just_transcript" not in st.session_state:
        st.session_state.whisper_just_transcript = default_whisper_just_transcript
    if "temporary_video_path" not in st.session_state:
        st.session_state.temporary_video_path = default_clip_video_path
    if "upload_url" not in st.session_state:
        st.session_state.upload_url = default_upload_url
    if "input_phrase" not in st.session_state:
        if st.session_state.upload_url == default_upload_url:
            st.session_state.input_phrase = default_input_phrase
        else:
            st.session_state.input_phrase = ""
    if "model_selection" not in st.session_state:
        st.session_state.model_selection = default_whisper_model_selection
    if "model_selection_index" not in st.session_state:
        st.session_state.model_selection_index = default_whisper_model_selection_index

    if "clip_video_paths" not in st.session_state:
        st.session_state.clip_video_paths = [default_clip_video_path] * 3
    if "clip_gif_paths" not in st.session_state:
        st.session_state.clip_gif_paths = [default_clip_gif_path] * 3
    if "recovered_phrases" not in st.session_state:
        st.session_state.recovered_phrases = [default_recovered_phrase] * 3
    if "gif_sizes" not in st.session_state:
        st.session_state.gif_sizes = [default_gif_size] * 3

    if "text_on_gif_val" not in st.session_state:
        st.session_state.text_on_gif_val = default_text_on_gif_val

    if "before_phrase_secs" not in st.session_state:
        st.session_state.before_phrase_secs = default_before_phrase_secs
    if "after_phrase_secs" not in st.session_state:
        st.session_state.after_phrase_secs = default_after_phrase_secs
    if "resize_factor" not in st.session_state:
        st.session_state.resize_factor = default_resize_factor
    if "fps" not in st.session_state:
        st.session_state.fps = default_fps
    if "use_whisper" not in st.session_state:
        st.session_state.use_whisper = False
    if "fetch_count" not in st.session_state:
        st.session_state.fetch_count = 0
    if "transcribe_count" not in st.session_state:
        st.session_state.transcribe_count = 0
    if "gif_expander" not in st.session_state:
        st.session_state.gif_expander = False


def reset_state(upload_url: str):
    st.session_state.yt_transcript_words = default_yt_transcript_words
    st.session_state.yt_just_transcript = default_yt_just_transcript
    st.session_state.whisper_transcript_words = default_whisper_transcript_words
    st.session_state.whisper_just_transcript = default_whisper_just_transcript
    st.session_state.model_selection = default_whisper_model_selection
    st.session_state.model_selection_index = default_whisper_model_selection_index
    st.session_state.clip_video_paths = [default_clip_video_path] * 3
    st.session_state.clip_gif_paths = [default_clip_gif_path] * 3
    st.session_state.recovered_phrases = [default_recovered_phrase] * 3
    st.session_state.gif_sizes = [default_gif_size] * 3
    st.session_state.fetch_count = 0
    st.session_state.transcribe_count = 0
    st.session_state.gif_expander = False
import streamlit as st
from yt_gif_maker.transcribe import avaliable_models
from yt_gif_maker.streamlit_funcs.state import init_state
from yt_gif_maker.streamlit_funcs.callbacks import fetch_logic, clip_and_gif, transcribe_logic, auto_usage


app_name = "YouTube gif maker"
st.set_page_config(page_title=app_name)
st.title(app_name)

init_state()


tab1, tab2, tab3 = st.tabs(["YouTube gif maker", "Advanced", "💡 About"])

with tab3:
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
            st.markdown("##### Enter url / line to gif / choose transcriber")
            cola, colb, colc = st.columns([6, 2, 2])
            with cola:
                upload_url = st.text_input(label="YouTube / Shorts url", value=st.session_state.upload_url, key="basic_upload", label_visibility="collapsed")
            with st.container(border=True):
                with colc:
                    st.session_state.use_whisper = st.checkbox(label="use whisper", value=False)
                with colb:
                    model_selection = st.selectbox(
                        label="whisper model",
                        index=st.session_state.model_selection_index,
                        options=avaliable_models,
                        key="auto_model",
                        disabled=False if st.session_state.use_whisper else True,
                        label_visibility="collapsed",
                    )
                    st.session_state.model_selection_index = avaliable_models.index(model_selection)
                    if st.session_state.model_selection != model_selection:
                        st.session_state.transcribe_count = 0
                        st.session_state.model_selection = model_selection                    
                    
            clip_input_col, clip_button_check = st.columns([3, 2])
            clip_button_col, emptya = st.columns([5, 1])

            with clip_input_col:
                st.session_state.input_phrase = st.text_input(
                    label="input phrase",
                    placeholder="enter in the input phrase you'd like gif-a-fied",
                    value=st.session_state.input_phrase,
                    max_chars=34,
                    label_visibility="collapsed",
                    key="auto_input_phrase"
                )
            with st.expander(label="gif size options"):
                with st.container(border=True):
                    (
                        clip_button_time_before_buffer,
                        clip_button_time_after_buffer,
                        clip_button_resize_factor,
                        clip_button_fps,
                    ) = st.columns([1, 1, 1, 1])
                with clip_button_check:
                    st.session_state.text_on_gif_val = st.checkbox("show input phrase on gif", value=st.session_state.text_on_gif_val, key="auto_text_on_gif_checkbox")
                with clip_button_time_before_buffer:
                    before_phrase_secs = st.number_input("include before (secs)", value=st.session_state.before_phrase_secs, min_value=0, max_value=20, key="auto_before_phrase_secs")
                with clip_button_time_after_buffer:
                    after_phrase_secs = st.number_input("include after (secs)", value=st.session_state.after_phrase_secs, min_value=0, max_value=20, key="auto_after_phrase_secs")
                with clip_button_resize_factor:
                    resize_factor = st.number_input("gif resize factor", value=st.session_state.resize_factor, min_value=0.1, max_value=1.0, key="auto_resize_factor")
                with clip_button_fps:
                    fps = st.number_input("gif fps", value=st.session_state.fps, min_value=10, max_value=60, key="auto_fps")

                with clip_button_col:
                    clip_button_val = st.button(
                        label="create gif",
                        type="primary",
                        on_click=auto_usage,
                        args=(upload_url, before_phrase_secs, after_phrase_secs, resize_factor, fps),
                        key="auto_clip_button"
                    )

            with st.expander(label="output gif", expanded=st.session_state.gif_expander):
                with st.container(border=True):
                    with st.container(border=True):
                        st.markdown("#### final gif")
                        st.image(st.session_state.clip_gif_paths[0], use_column_width="always")
                    st.text_input(label="gif size (in MBs)", value=st.session_state.gif_sizes[0], key="auto_gif")

                    with open(st.session_state.clip_gif_paths[0], "rb") as file:
                        btn = st.download_button(
                            label="download gif", data=file, file_name=f"{st.session_state.input_phrase}.gif", mime="image/gif", key="auto_gif_download", type="primary"
                        )

                    with st.container(border=True):
                        st.markdown("#### raw video clip")
                        st.video(st.session_state.clip_video_paths[0])





### advanced tab ###
with tab2:
    with st.container(border=True):
        with st.container(border=True):
            st.markdown("#### upload area")
            upload_url = st.text_input(label="YouTube / Shorts url", value=st.session_state.upload_url)
            yt_fetch_button = st.button(
                label="fetch video",
                type="secondary",
                on_click=fetch_logic,
                args=(upload_url, ),
            )

        col_video_empty_1, col_orig_video, col_video_empty_2 = st.columns([4, 8, 4])
        with col_orig_video:
            with st.container(border=True):
                st.caption("original video")
                st.video(st.session_state.temporary_video_path)

    with st.container(border=True):
        st.markdown("#### transcript area")
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
            
            model_selection = st.selectbox(
                label="whisper model (base only in HF space)",
                index=st.session_state.model_selection_index,
                options=avaliable_models,
            )
            st.session_state.model_selection_index = avaliable_models.index(model_selection)
            if st.session_state.model_selection != model_selection:
                st.session_state.transcribe_count = 0
                st.session_state.model_selection = model_selection           

            trans_button_val = st.button(
                label="transcribe with whisper",
                type="secondary",
                on_click=transcribe_logic,
                args=(),
            )

    with st.container(border=True):
        st.markdown("#### clip / gif maker area")

        with st.container(border=True):
            clip_input_col, clip_button_col, clip_button_check = st.columns([2, 1, 2])

        with clip_input_col:
            st.session_state.input_phrase = st.text_input(
                label="input phrase",
                placeholder="enter in the input phrase you'd like gif-a-fied",
                value=st.session_state.input_phrase,
                max_chars=34,
                label_visibility="collapsed",
            )
        with st.container(border=True):
            (
                clip_button_time_before_buffer,
                clip_button_time_after_buffer,
                clip_button_resize_factor,
                clip_button_fps,
            ) = st.columns([1, 1, 1, 1])
        with clip_button_check:
            st.session_state.text_on_gif_val = st.checkbox("show input phrase on gif", value=st.session_state.text_on_gif_val)
        with clip_button_time_before_buffer:
            before_phrase_secs = st.number_input("include before (secs)", value=st.session_state.before_phrase_secs, min_value=0, max_value=5)
        with clip_button_time_after_buffer:
            after_phrase_secs = st.number_input("include after (secs)", value=st.session_state.after_phrase_secs, min_value=0, max_value=5)
        with clip_button_resize_factor:
            resize_factor = st.number_input("gif resize factor", value=st.session_state.resize_factor, min_value=0.1, max_value=1.0)
        with clip_button_fps:
            fps = st.number_input("gif fps", value=st.session_state.fps, min_value=10, max_value=60)

        with clip_button_col:
            clip_button_val = st.button(
                label="phrase-clip",
                type="secondary",
                on_click=clip_and_gif,
                args=(before_phrase_secs, after_phrase_secs, resize_factor, fps, 3),
            )

        col_clip_1, col_gif_1 = st.columns([4, 4])
        col_clip_2, col_gif_2 = st.columns([4, 4])
        col_clip_3, col_gif_3 = st.columns([4, 4])

        with st.container(border=True):
            with col_clip_1:
                with st.container(border=True):
                    st.markdown("#### video from clip 1")
                    st.video(st.session_state.clip_video_paths[0])
                st.text_input(label="similar phrase", value=st.session_state.recovered_phrases[0], key=0)

            with col_gif_1:
                with st.container(border=True):
                    st.markdown("#### gif from clip 1")
                    st.image(st.session_state.clip_gif_paths[0])
                st.text_input(label="gif size (in MBs)", value=st.session_state.gif_sizes[0], key=10)

                with open(st.session_state.clip_gif_paths[0], "rb") as file:
                    btn = st.download_button(
                        label="download gif", data=file, file_name=f"{st.session_state.input_phrase}.gif", mime="image/gif", key=20
                    )

        with st.container(border=True):
            with col_clip_2:
                with st.container(border=True):
                    st.markdown("#### video from clip 2")
                    st.video(st.session_state.clip_video_paths[1])
                st.text_input(label="similar phrase", value=st.session_state.recovered_phrases[1], key=1)

            with col_gif_2:
                with st.container(border=True):
                    st.markdown("#### gif from clip 2")
                    st.image(st.session_state.clip_gif_paths[1])
                st.text_input(label="gif size (in MBs)", value=st.session_state.gif_sizes[0], key=11)

                with open(st.session_state.clip_gif_paths[1], "rb") as file:
                    btn = st.download_button(
                        label="download gif", data=file, file_name=f"{st.session_state.input_phrase}.gif", mime="image/gif", key=21
                    )

        with st.container(border=True):
            with col_clip_3:
                with st.container(border=True):
                    st.markdown("#### video from clip 3")
                    st.video(st.session_state.clip_video_paths[2])
                st.text_input(label="similar phrase", value=st.session_state.recovered_phrases[2], key=2)

            with col_gif_3:
                with st.container(border=True):
                    st.markdown("#### gif from clip 3")
                    st.image(st.session_state.clip_gif_paths[2])
                st.text_input(label="gif size (in MBs)", value=st.session_state.gif_sizes[2], key=12)

                with open(st.session_state.clip_gif_paths[2], "rb") as file:
                    btn = st.download_button(
                        label="download gif", data=file, file_name=f"{st.session_state.input_phrase}.gif", mime="image/gif", key=22
                    )

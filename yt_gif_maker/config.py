import uuid


# initial state values
default_yt_transcript_words = None
default_yt_just_transcript = None
default_whisper_transcript_words = None
default_whisper_just_transcript = None
default_upload_url = "https://www.youtube.com/watch?v=svX9-fYMIQU"
default_input_phrase = "bitches leave"
default_whisper_model_selection = "base"
default_whisper_model_selection_index = 1
default_clip_video_path = "./data/input/blank.mp4"
default_clip_gif_path = "./data/input/blank.jpg"
default_recovered_phrase = ""
default_gif_size = ""
default_text_on_gif_val = True
default_before_phrase_secs = 0
default_after_phrase_secs = 0
default_resize_factor = 0.2
default_fps = int(15)


def default_temp_video_location():
    return "/original_" + str(uuid.uuid4()) + ".mp4"

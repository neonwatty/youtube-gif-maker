from yt_gif_maker.transcribe import transcribe
from yt_gif_maker.nearest import get_nearest_snippets
from yt_gif_maker.gif_maker import clip_video_and_gif, draw_on_gif


def process():
    video_file_path = "data/input/bleep_test_1.mp4"
    transcript, timestamped_words = transcribe(video_file_path);

    query = "every time we to go costa rica"
    closest_time_ranges = get_nearest_snippets(query, transcript, timestamped_words) 

    output_clip_path = "test.mp4"
    output_gif_path = "test.gif"
    start_ms = closest_time_ranges[0][0]
    end_ms = closest_time_ranges[0][1]
    clip_video_and_gif(video_file_path, output_clip_path, output_gif_path, start_ms, end_ms)

    input_gif_path = "test.gif"
    output_gif_path = "test_with_writing.gif"
    text = "HEY LOOK MOM NO HANDS"
    draw_on_gif(input_gif_path, output_gif_path, text)
    
if __name__ =="__main__":
    process()
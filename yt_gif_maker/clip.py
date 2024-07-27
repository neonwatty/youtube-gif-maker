from moviepy.video.io.VideoFileClip import VideoFileClip


def clip_video(video_file_path: str, output_clip_path: str, start_ms: int, end_ms: int, before_secs: float, after_secs: float):
    start_time = start_ms / 1000.0 - before_secs
    end_time = end_ms / 1000.0 + after_secs
    video = VideoFileClip(video_file_path)
    subclip = video.subclip(start_time, end_time)
    subclip.write_videofile(output_clip_path, codec="libx264", audio_codec="aac")
    video.close()

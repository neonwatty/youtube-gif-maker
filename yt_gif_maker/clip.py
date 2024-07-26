from moviepy.video.io.VideoFileClip import VideoFileClip


def clip_video(video_file_path: str, output_clip_path: str, start_ms: int, end_ms: int):
    start_time = start_ms / 1000.0
    end_time = end_ms / 1000.0
    video = VideoFileClip(video_file_path)
    subclip = video.subclip(start_time, end_time)
    subclip.write_videofile(output_clip_path, codec="libx264", audio_codec="aac")
    video.close()

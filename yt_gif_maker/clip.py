from moviepy.video.io.VideoFileClip import VideoFileClip


def clip_video(video_file_path: str, output_clip_path: str, start_ms: int, end_ms: int, before_secs: float, after_secs: float):
    video = VideoFileClip(video_file_path)
    video_length_seconds = video.duration
    
    start_time = max(start_ms / 1000.0 - before_secs, 0)
    end_time = min(end_ms / 1000.0 + after_secs, video_length_seconds)

    subclip = video.subclip(start_time, end_time)
    subclip.write_videofile(output_clip_path, codec="libx264", audio_codec="aac")
    video.close()

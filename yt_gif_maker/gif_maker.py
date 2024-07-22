from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image, ImageDraw, ImageSequence
import io


def clip_video_and_gif(video_file_path: str, 
                       output_clip_path: str,
                       output_gif_path: str,
                       start_ms: int, 
                       end_ms: int):
    start_time = start_ms / 1000.0
    end_time = end_ms / 1000.0
    video = VideoFileClip(video_file_path)
    subclip = video.subclip(start_time, end_time)
    subclip.write_videofile(output_clip_path, codec="libx264", audio_codec="aac")
    video.write_gif(output_gif_path,fps=25, program='ffmpeg')
    video.close()


def draw_on_gif(input_gif_path: str, output_gif_path: str, text) -> None:
    im = Image.open(input_gif_path)

    # A list of the frames to be outputted
    frames = []
    # Loop over each frame in the animated image
    for frame in ImageSequence.Iterator(im):
        # Draw the text on the frame
        d = ImageDraw.Draw(frame)
        d.text((10,100), text)
        del d

        # However, 'frame' is still the animated image with many frames
        # It has simply been seeked to a later frame
        # For our list of frames, we only want the current frame

        # Saving the image without 'save_all' will turn it into a single frame image, and we can then re-open it
        # To be efficient, we will save it to a stream, rather than to file
        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)

        # Then append the single frame image to a list of frames
        frames.append(frame)
    # Save the frames as a new image
    frames[0].save(output_gif_path, save_all=True, append_images=frames[1:])
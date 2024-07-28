from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image, ImageDraw, ImageFont


def resize_frame(frame, scale_factor=0.5):
    width, height = frame.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return frame.resize((new_width, new_height), Image.Resampling.LANCZOS)


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def draw_text_on_gif(input_gif_path, output_gif_path, input_phrase):
    # Open the GIF file
    with Image.open(input_gif_path) as img:
        # Ensure the image is a GIF
        if img.format != "GIF":
            raise ValueError("The provided file is not a GIF.")

        frames = []
        try:
            while True:
                # Create a copy of the frame
                frame = img.copy()

                # draw
                draw = ImageDraw.Draw(frame)

                # Calculate the maximum width for each line of text
                width, height = frame.size
                max_line_width = width * 0.9  # 90% of frame width for some padding

                # Load a larger font (size 5 times larger)
                try:
                    font_size = int(width * 0.075)  # 3 * 10  # Example: base size 10
                    font = ImageFont.truetype("./yt_gif_maker/arial.ttf", font_size)
                except IOError:
                    raise IOError("Font file not found.")

                # Split the text into two lines
                def split_text(text, max_width, font):
                    lines = []
                    words = text.split()
                    current_line = ""

                    for word in words:
                        test_line = f"{current_line} {word}".strip()
                        if textsize(test_line, font=font)[0] <= max_width:
                            current_line = test_line
                        else:
                            if current_line:
                                lines.append(current_line)
                            current_line = word

                    if current_line:
                        lines.append(current_line)

                    return lines

                lines = split_text(input_phrase, max_line_width, font)

                if len(lines) > 2:
                    lines = lines[:2]  # Keep only the first two lines if more are present

                # Calculate the height needed for all lines
                text_height = sum(textsize(line, font=font)[1] for line in lines)

                # Position the text in the lower third of the frame
                y = height * 2 / 3
                y = min(y, height - text_height)  # Adjust if needed

                # Draw each line of text
                for line in lines:
                    text_width, line_height = textsize(line, font=font)
                    x = (width - text_width) / 2
                    
                    # Define outline width
                    outline_width = 1

                    # Draw outline (black)
                    for offset in range(-outline_width, outline_width + 1):
                        draw.text((x + offset, y), line, font=font, fill="black")
                        draw.text((x - offset, y), line, font=font, fill="black")
                        draw.text((x, y + offset), line, font=font, fill="black")
                        draw.text((x, y - offset), line, font=font, fill="black")
                    
                    draw.text((x, y), line, font=font, fill="white")
                    y += line_height

                # Append the frame to the list of frames
                frames.append(frame)

                # Move to the next frame
                img.seek(img.tell() + 1)
        except EOFError:
            pass  # End of frames

        # Save the modified frames as a new GIF
        frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], loop=0)


def create_resized_gif(input_gif_path, output_gif_path, scale_factor=0.5):
    with Image.open(input_gif_path) as img:
        frames = []
        try:
            while True:
                frame = img.copy()
                resized_frame = resize_frame(frame, scale_factor)
                frames.append(resized_frame)
                img.seek(img.tell() + 1)
        except EOFError:
            pass  # End of frames

        # Save the resized frames as a new GIF
        frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], loop=0)


def make_gif(video_file_path: str, output_gif_path: str, input_phrase: str, text_on_gif_val: bool, resize_factor: float, fps: int) -> None:
    video = VideoFileClip(video_file_path)
    video.write_gif(output_gif_path, fps=fps, program="ffmpeg")
    create_resized_gif(output_gif_path, output_gif_path, resize_factor)
    if text_on_gif_val:
        draw_text_on_gif(output_gif_path, output_gif_path, input_phrase)


def clip_video_and_gif(video_file_path: str, output_clip_path: str, output_gif_path: str, start_ms: int, end_ms: int):
    start_time = start_ms / 1000.0
    end_time = end_ms / 1000.0
    video = VideoFileClip(video_file_path)
    subclip = video.subclip(start_time, end_time)
    subclip.write_videofile(output_clip_path, codec="libx264", audio_codec="aac")
    video.write_gif(output_gif_path, fps=25, program="ffmpeg")
    video.close()

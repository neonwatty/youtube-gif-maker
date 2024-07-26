import re
from youtube_transcript_api import YouTubeTranscriptApi


def estimate_word_times_proportional(data: list) -> list:
    result = []
    for entry in data:
        phrase = entry['text']
        start = entry['start']
        duration = entry['duration']
        
        words = phrase.split()
        total_chars = sum(len(word) for word in words)
        
        if total_chars == 0:
            continue        
        word_start = start
        
        for word in words:
            word_chars = len(word)
            word_duration = (word_chars / total_chars) * duration
            word_stop = word_start + word_duration
            
            result.append({
                'word': word,
                'start': round(word_start, 2),
                'end': round(word_stop, 2)
            })            
            word_start = word_stop
    return result


def is_valid_youtube_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    pattern = r"^https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}$"  # youtube vido ids are always 11 chars long
    if "shorts" in url:
        pattern = r"^https://www\.youtube\.com/shorts/[A-Za-z0-9_-]{11}$"  # youtube vido ids are always 11 chars long
    return re.match(pattern, url) is not None


def get_single_transcript(youtube_url: str) -> dict:
    try:
        if is_valid_youtube_url(youtube_url):
            if "=" in youtube_url:
                video_id = youtube_url.split("=")[-1]
            else:
                video_id = youtube_url.split("/")[-1]
            video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_words = estimate_word_times_proportional(video_transcript)
            entry = {}
            entry["youtube_url"] = youtube_url
            entry["video_id"] = video_id
            entry["transcript"] = " ".join([v["text"] for v in video_transcript])
            entry["transcript_words"] = transcript_words
            return entry
        else:
            print(f"FAILURE: youtube_url is not valid - {youtube_url}")
            return {}
    except Exception as e:
        print(f"FAILURE: transcript pull for youtube_url - {youtube_url} - failed with exception {e}")
        return {}

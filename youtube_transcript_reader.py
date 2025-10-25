from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript_from_youtube_url(url):
    """
    Extracts the video ID from a YouTube URL and fetches its transcript.
    """
    try:
        video_id = url.split("v=")[1].split("&")[0]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        return transcript
    except Exception as e:
        print(f"Error fetching YouTube transcript: {e}")
        return None
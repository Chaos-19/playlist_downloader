from app import celery
import yt_dlp

@celery.task
def fetch_metadata(ytv_url):
    """Fetch YouTube metadata asynchronously."""
    with yt_dlp.YoutubeDL({}) as ydl:
        return ydl.extract_info(ytv_url, download=False)
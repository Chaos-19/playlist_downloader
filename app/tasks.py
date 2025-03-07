import os
import zipfile
import yt_dlp
from app import celery

@celery.task
def fetch_metadata(ytv_url):
    """Fetch YouTube metadata asynchronously."""
    with yt_dlp.YoutubeDL({}) as ydl:
        return ydl.extract_info(ytv_url, download=False)

@celery.task
def download_ytv_and_zip(ytv_url):
    """Download and ZIP videos asynchronously."""
    ydl_opts = {"outtmpl": "download/%(title)s.%(ext)s"}
    
    download_title = ""
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(ytv_url, download=False)
        download_title = info.get("title", "Unknown Playlist")
        
        ydl.download([ytv_url])
    
    zip_path = os.path.join(f"{download_title}.zip")
    zip_folder.apply_async(args=["download", zip_path])
    return f"Downloading {download_title} and zipping..."

@celery.task
def zip_folder(folder_path, zip_filename):
    """Zip all files inside the folder."""
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Keep folder structure
                zipf.write(file_path, arcname)
    return f"Zipped {zip_filename}"
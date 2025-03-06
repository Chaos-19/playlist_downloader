import yt_dlp

import zipfile
import os
import json

def download_yt_video_and_ZIP(URL):
    ydl_opts = {"outtmpl": "download/%(title)s.%(ext)s"}
    
    download_title = ""
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        download_title = info.get("title", "Unknown Playlist")
        
        ydl.download([URL])
    
    zip_folder("download", f"{download_title}.zip")    
    
    
def zip_folder(folder_path, zip_filename):
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Keep folder structure
                zipf.write(file_path, arcname)


download_yt_video_and_ZIP("https://youtube.com/playlist?list=PLo9DFPAX3cBprVElqCLtDDlpSiYTlEnVh&si=Q6Wkdmy_BBMxcraK")


import yt_dlp

playlist_url = "https://youtube.com/playlist?list=PL0vfts4VzfNjurgyRawm_e0RevgP7g1Ao"

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(playlist_title)s/%(title)s.%(ext)s",  # Organized in folder
    "extract_audio": True,  # Extract audio only
    "audio_format": "mp3",  # Convert to MP3
    "audio_quality": "192K",  # Set audio quality
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])
    
ydl_opts = {
    "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",  # Limit to 720p
    "outtmpl": "%(playlist_title)s/%(title)s.%(ext)s",
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])
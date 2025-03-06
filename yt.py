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
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from dotenv import load_dotenv # type: ignore
import os
import yt_dlp

import zipfile
import os
import json

load_dotenv()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def fetch_metadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch YouTube metadata asynchronously."""
    ytv_url = "https://youtube.com/watch?v=-qjE8JkIVoQ&si=QeI-Vt4JGxV6Sr9Y"
    with yt_dlp.YoutubeDL({}) as ydl:
        result = ydl.extract_info(ytv_url, download=False)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result.get("title", "Unknown Playlist"))
        
        
async def download_ytv_and_zip(ytv_url):
    """Download and ZIP videos asynchronously."""
    ydl_opts = {"outtmpl": "download/%(title)s.%(ext)s"}
    
    download_title = ""
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(ytv_url, download=False)
        download_title = info.get("title", "Unknown Playlist")
        
        ydl.download([ytv_url])
    
    zip_path = os.path.join(f"{download_title}.zip")
    #zip_folder.apply_async(args=["download", zip_path])
    
    return f"Downloading {download_title} and zipping..."

async def zip_folder(folder_path, zip_filename):
    """Zip all files inside the folder."""
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Keep folder structure
                zipf.write(file_path, arcname)
    return f"{zip_filename}"

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    ytv_metadata_handler = CommandHandler('info', fetch_metadata)
    
    application.add_handler(start_handler)
    application.add_handler(ytv_metadata_handler)
    
    application.run_polling()
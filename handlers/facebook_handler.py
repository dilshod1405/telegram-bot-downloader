import os
from aiogram import types, Router, F
import yt_dlp
from aiogram.types import InputFile

router = Router()

class MediaFile(InputFile):
    def __init__(self, path):
        super().__init__(path)
        self.path = path

    def read(self, bot):
        with open(self.path, 'rb') as f:
            return f.read()

@router.message(F.text.regexp(r'https://www.facebook.com/'))
async def facebook_handler(message: types.Message):
    url = message.text.strip()

    await message.reply("Iltimos, kutib turing. Video yuklanmoqda ... ⏳")

    # Set download options and define output path
    download_path = "downloads/facebook_video.mp4"
    ydl_opts = {
        "format": "mp4",
        "outtmpl": download_path,
    }

    try:
        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Check if the file was downloaded and is non-empty
        if os.path.exists(download_path) and (os.path.getsize(download_path) > 0 and os.path.getsize(download_path) <= 50 * 1024 * 1024):
            # Send video to the user
            with open(download_path, 'rb') as f:
                media_file = MediaFile(f.name)
                await message.reply_video(media_file, caption="🎥 Marhamat buyurtmangiz tayyor ✅")

            # Clean up downloaded file
            os.remove(download_path)
        
        elif os.path.exists(download_path) and os.path.getsize(download_path) > 50 * 1024 * 1024:
            await message.reply("Videoning hajmi 50 MB dan oshmasligi kerak ❗️")
            
        else:
            await message.reply("Could not download the media. Please ensure the link is correct or the video is publicly accessible.")

    except Exception as e:
        await message.reply(f"Error downloading Facebook video: {e}")

import yt_dlp as ytdlp
import os
from aiogram import types, Router, F
from aiogram.types import InputFile

# Define the download directory
download_dir = "downloads"

# Ensure the directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir, exist_ok=True)


# Store the file_id once the video is uploaded (this can be stored in a database or file)
video_file_ids = {}

# Create a Router instance for handling the messages
router = Router()


class VideoFile(InputFile):
    def __init__(self, filename):
        self.filename = filename
        self.size = os.path.getsize(filename)
    
    def read(self, bot):
        with open(self.filename, 'rb') as f:
            return f.read()


@router.message(F.text.regexp(r'https://www.youtube.com/'))
async def check_youtube_link(message: types.Message):
    url = message.text
    await message.reply("Kutib turing, havola orqali video va audio yuklanmoqda ... ⏳")
    if url.startswith('https://www.youtube.com/'):
        await message.reply("Sahifaning havolasini yuboryapsiz. Videoning havolasini yuboring ❗️")
    else:
        pass

@router.message(F.text.regexp(r'https://youtu.be/'))    
async def handle_youtube_link(message: types.Message):
    url = message.text
    await message.reply("Kutib turing, havola orqali video va audio yuklanmoqda ... ⏳")


    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_dir, 'video.mp4'),
            'noplaylist': True,
            'quiet': False,
            'restrictfilenames': True,
            'username': 'dilshod1405',
            'password': 'dilshod0514'
        }

        ydl_opts2 = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_dir, 'audio.mp3'),
            'noplaylist': True,
            'quiet': False,
            'restrictfilenames': True,
            'username': 'dilshod1405',
            'password': 'dilshod0514'
        }

        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Attempting to download video from URL: {url}")
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            print(f"Video filename: {filename}")

        
            
        if os.path.exists(filename):
                # Check the file size
                file_size = os.path.getsize(filename)
                if file_size > 50 * 1024 * 1024:
                    await message.reply("Videoning hajmi 50 MB dan oshmasligi kerak ❗️")
                else:
                    # If the file is small enough, send it to the user
                    with open(filename, 'rb') as video_file:
                        video = VideoFile(filename)
                        await message.reply_video(video, caption="🎥 Marhamat buyurtmangiz tayyor ✅")
                        await message.reply_audio(video, caption="🎧 Marhamat buyurtmangiz tayyor ✅")

                # Clean up by removing the downloaded video
                formats = ['.mp4', '.mp3']
                for format in formats:
                    file_path = os.path.join(download_dir, f'video{format}')
                    if os.path.exists(file_path):
                        os.remove(file_path)
        else:
            print("Error: Video file not found.")
            await message.reply("Havola bo'yicha video topilmadi.")
    except Exception as e:
        print(f"Error during download: {e}")
        await message.reply(f"Xatolik: {e}")

    

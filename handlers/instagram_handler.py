import os
import instaloader
from aiogram import types, Router, F
from aiogram.types import InputFile
from moviepy.editor import VideoFileClip

router = Router()  # Create router for Instagram handler


class MediaFile(InputFile):
    def __init__(self, path):
        super().__init__(path)
        self.path = path

    def read(self, bot):
        with open(self.path, 'rb') as f:
            return f.read()
    

@router.message(F.text.regexp(r'https://www.instagram.com/')) 
async def instagram_handler(message: types.Message):
    url = message.text

    await message.reply("Iltimos, kutib turing. Video yuklanmoqda ... ⏳")

    # Set up instaloader
    L = instaloader.Instaloader(dirname_pattern="downloads", filename_pattern="{shortcode}", save_metadata=False)

    try:
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        L.download_post(post, target="downloads")

        # Determine if media is a video or a photo
        media_file_path = f"downloads/{post.shortcode}.mp4"
        
        # Check size of media file
        if os.path.getsize(media_file_path) > 50 * 1024 * 1024:
            await message.reply("Videoning hajmi 50 MB dan oshmasligi kerak ❗️")
        elif os.path.exists(media_file_path) and os.path.getsize(media_file_path) <= 50 * 1024 * 1024:
            with open(media_file_path, 'rb') as f:
                media_file = MediaFile(f.name)
                audio_file = os.path.splitext(media_file_path)[0] + ".mp3"
                clip = VideoFileClip(media_file_path)
                clip.audio.write_audiofile(audio_file)
                await message.reply_video(media_file, caption="🎥 Marhamat buyurtmangiz tayyor ✅")
                await message.reply_audio(audio_file)

                
            # Delete the downloaded media file
            formats = ['.mp4', '.jpg', '.png', '.txt', '.mp3']
            for format in formats:
                file_path = f"downloads/{post.shortcode}{format}"
                if os.path.exists(file_path):
                    os.remove(file_path)
        else:
            await message.reply("Could not download the media. Please ensure the link is correct.")

    except Exception as e:
        await message.reply(f"Error downloading Instagram media: {e}")

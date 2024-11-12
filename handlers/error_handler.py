from aiogram import types, Router, F

router = Router()

@router.message(F.text.regexp(r'https://'))
async def unsupported_url_handler(message: types.Message):
    # Check if the message contains a URL but is not from a supported platform
    url = message.text.strip().lower()
    if not any(domain in url for domain in ["youtube.com", "youtu.be", "instagram.com", "www.facebook.com"]):
        await message.reply("Kechirasiz, ushbu veb saytdan media yuklash xizmati mavjud emas. Faqat YouTube, Instagram va Facebook ijtimoiy tarmoqlari orqali yuklash imkoni mavjud.")

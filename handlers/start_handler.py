from aiogram import types, Router, F
from aiogram.filters import CommandStart
from keyboards import platform_keyboard

router = Router()

# Dictionary to track users' platform choices
user_choices = {}

@router.message(CommandStart())
async def start(message: types.Message):
    await message.reply("Ijtimoiy tarmoqni tanlang:", reply_markup=platform_keyboard)

@router.message(F.text.in_({"YouTube", "Instagram", "Facebook"}))
async def platform_choice(message: types.Message):
    platform = message.text
    user_choices[message.from_user.id] = platform  # Store the user's platform choice
    await message.reply(f"{platform} post havolasini yuboring.")

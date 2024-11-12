from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Define the keyboard with a list of lists containing `KeyboardButton` objects
platform_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='YouTube')],
        [KeyboardButton(text='Instagram')],
        [KeyboardButton(text='Facebook')]
    ],
    resize_keyboard=True
)

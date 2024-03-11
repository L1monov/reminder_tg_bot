from aiogram import Router, Bot, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboards(text):
    if isinstance(text, str):
        text = [text]


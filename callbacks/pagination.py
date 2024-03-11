from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class Pagination(CallbackData, prefix ='pag'):
    page: int
    action: str


def paginator(dict_reminder: dict, page: int = 0):
    builder = InlineKeyboardBuilder()
    for _ in range((page*5)+1, (page*5)+6):
        try:
            builder.button(text=str(_), callback_data=f"info_{dict_reminder[_]['token']}")
        except:
            continue
    if page == 0:
        builder.row(
            InlineKeyboardButton(text='Следущаяя', callback_data=Pagination(action='next', page=page).pack()),
            width=1
        )
    if page != 0:
        if len(dict_reminder) <= (page+1)*5:
            builder.row(
                InlineKeyboardButton(text='Предыдущая', callback_data=Pagination(action='prev', page=page).pack()),
                width=1
            )
        else:
            builder.row(
                InlineKeyboardButton(text='Предыдущая', callback_data=Pagination(action='prev', page=page).pack()),
                InlineKeyboardButton(text='Следущаяя', callback_data=Pagination(action='next', page=page).pack()),
                width=2
            )
    return builder.as_markup()
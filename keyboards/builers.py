from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton

def create_builder_inline(dict_for_button: dict, max_button_on_row: int = 1):
    # Example dict
    # dict_example = {
    #         'text': 'callback',
    #         'Все пользователи': 'list_users'
    # }
    builder = InlineKeyboardBuilder()
    current_button_count = 0  # Счетчик кнопок в текущей строке

    [builder.button(text=txt, callback_data=callback) for txt, callback in dict_for_button.items()]
    builder.adjust(max_button_on_row)
    return builder.as_markup()


def create_builder_reply(text: str | list, max_buttons_in_line: int = 1):

    if isinstance(text, str):
        text = [text]

    builder = ReplyKeyboardBuilder()

    [builder.add(KeyboardButton(text=txt)) for txt in text]
    builder.adjust(max_buttons_in_line)
    return builder.as_markup(resize_keyboard=True)

# def create_builder_for_list_reminder(range_dict_reminder: int, dict_reminder: dict):
#
#     builder = InlineKeyboardBuilder()
#
#     for _ in range(1, range_dict_reminder):
#         builder.button(
#             text=str(_),
#             callback_data=f"info_{dict_reminder[_]['token']}"
#         )
#     builder.button(
#         text='Следущая',
#         callback_data='test'
#     )
#     builder.button(
#         text='Предыдущая',
#         callback_data='test'
#     )
#     builder.adjust(5, 2)
#
#     return builder.as_markup()
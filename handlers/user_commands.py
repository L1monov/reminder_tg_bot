from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, Bot, F
from keyboards import reply, builers
import texts
from settings import dict_text_for_button
from data.database import My_Database
from handlers import heander_message
import datetime
from callbacks import pagination
from defs import defs


router = Router()

@router.message(Command(commands=["start"]))
async def start(message: Message, bot: Bot):

    db = My_Database()

    reply_inline = builers.create_builder_inline(
        dict_for_button={
            dict_text_for_button['inline_buttons']['start_tutorial']: 'start_tutorial',
            dict_text_for_button['inline_buttons']['i_know_everythings']: 'i_know_everything'
        },
        max_button_on_row=2
    )

    reply_reply = builers.create_builder_reply(
        text=[dict_text_for_button['reply_buttons']['add_rem'], dict_text_for_button['reply_buttons']['all_rem']],
        max_buttons_in_line=1
    )
    await message.answer(f"Привет, {message.from_user.first_name}", reply_markup=reply_reply)
    await message.answer(f"{texts.msg_start}", reply_markup=reply_inline)
    tg_id = message.from_user.id
    tg_nickname = message.from_user.username
    db.insert_one_user(tg_id=tg_id, tg_nickname=tg_nickname)


@router.message(F.text == '➕Добавить')
async def all_message(message: Message):
    msg = texts.msg_for_button_add
    await message.answer(msg)

@router.message(F.text == '🧾Лист напоминаний')
async def all_message(message: Message):
    db = My_Database()
    dict_reminder = db.get_all_reminder(message.from_user.id)
    msg = ''
    for _ in range(1,6):
        try:
            msg += f"{_}) {dict_reminder[_]['text']} (Напоминть {dict_reminder[_]['date_rim']})\n"
        except:
            pass
    msg += '\n\nВыберите номер для его редактирования'
    reply = pagination.paginator(dict_reminder=dict_reminder)
    await message.answer(msg, reply_markup=reply)


@router.message()
async def all_message(message: Message):
    db = My_Database()
    info_message = heander_message.handlers_message(message.text)
    if info_message['status'] == 'no text':
        await message.answer('Вы не ввели текст')
        return
    if info_message['status'] == 'no date':
        await message.answer(text=texts.msg_for_no_date)
        return
    if info_message['status'] == 'nice':
        specified_datetime = datetime.datetime.strptime(info_message['date'], '%Y-%m-%d %H:%M')
        current_datetime = datetime.datetime.now()

        if specified_datetime < current_datetime:
            await message.answer('Вы указали прошеднее время. Проверьте ещё раз дату!')
            return

        info_user = db.get_info_user(message.from_user.id)
        random_token = defs.create_token_for_rem(info_user['id'])
        text_msg = f"""Напоминание добавлено на <b>{info_message['date']}</b>\nТекст напоминания: <b>{info_message['text']}</b>"""
        db.insert_reminder(id_user=info_user['id'], token=random_token, text=info_message['text'],date_rim=info_message['date'])
        reply = builers.create_builder_inline(dict_for_button={
            'Посмотреть информацию': f'info_{random_token}'
        })
        await message.answer(
            text=text_msg,
            reply_markup=reply
        )








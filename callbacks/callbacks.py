from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
import texts
from data import database
from keyboards import builers
from . import pagination
import settings
from data.database import My_Database

router = Router()


@router.callback_query(F.data == 'start_tutorial')
async def start_tutorial(call: CallbackQuery):
    print(call.data)
    await call.message.edit_text(
        text=texts.msg_help
    )
    await call.answer()


@router.callback_query(pagination.Pagination.filter(F.action.in_(['prev', 'next'])))
async def pagination_handler(call: CallbackQuery, callback_data: pagination.Pagination):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0
    if callback_data.action == 'next':
        page = page_num + 1
    db = My_Database()
    dict_reminder = db.get_all_reminder(call.from_user.id)
    msg = ''
    for _ in range(page*5+1, page*5+6):
        try:
            msg += f"{_}) {dict_reminder[_]['text']} (Напомнить {dict_reminder[_]['date_rim']})\n"
        except:
            continue
    msg += '\n\nВыберите номер для его редактирования'
    reply = pagination.paginator(dict_reminder=dict_reminder, page=page)
    await call.message.edit_text(
        text=f'{msg}',
        reply_markup= reply
    )

@router.callback_query()
async def handle_callback(call: CallbackQuery):
    db = database.My_Database()
    call_data = call.data.split('_')

    if call.data == 'i_know_everything':
        await call.message.edit_text(
            text=texts.msg_i_know_everything
        )

    if call.data == 'list_reminder':
        dict_reminder = db.get_all_reminder(call.from_user.id)
        msg = ''
        for _ in range(1, 6):
            msg += f"{_}) {dict_reminder[_]['text']} (Напомнить {dict_reminder[_]['date_rim']})\n"
        msg += '\n\nВыберите номер для его редактирования'
        reply = pagination.paginator(dict_reminder=dict_reminder)
        await call.message.edit_text(msg, reply_markup=reply)

    if 'info' in call_data: # обратботка info  выдаём инфу о напоминании

        full_token = call.data.replace('info_', '')
        token_rim = full_token[:-20]
        id_user = full_token.replace(token_rim, '')
        info_reminder = db.get_info_reminder(full_token)
        msg_info_reminder = f"""{info_reminder['text']}\n\n<b>Время отправки:</b> {info_reminder['date_rim']}"""
        reply = builers.create_builder_inline(dict_for_button={
            # settings.dict_text_for_button['inline_buttons']['deactivate']: f'editrim_deactivate_{full_token}',
            settings.dict_text_for_button['inline_buttons']['delete_riminder']: f'editrim_delete_{full_token}',
            settings.dict_text_for_button['inline_buttons']['all_reminder']: 'list_reminder'
        },
        max_button_on_row=1
        )

        await call.message.edit_text(
            text=msg_info_reminder,
            reply_markup=reply
        )

    if 'editrim' in call_data:
        full_token = call_data[2]
        # if 'deactivate' in call_data:
        #     db.deactivate_reminder(token=full_token)
        #     reply = builers.create_builder_inline(dict_for_button={
        #         settings.dict_text_for_button['inline_buttons']['deactivate']: f'editrim_activate_{full_token}',
        #         settings.dict_text_for_button['inline_buttons']['delete_riminder']: f'editrim_delete_{full_token}',
        #         settings.dict_text_for_button['inline_buttons']['all_reminder']: 'list_reminder'
        #     },
        #         max_button_on_row=2
        #     )
        #     await call.message.edit_text(text='Напоминание выключено', reply_markup=reply)
        # if 'activate' in call_data:
        #     db.deactivate_reminder(token=full_token)
        #     reply = builers.create_builder_inline(dict_for_button={
        #         settings.dict_text_for_button['inline_buttons']['deactivate']: f'editrim_deactivate_{full_token}',
        #         settings.dict_text_for_button['inline_buttons']['delete_riminder']: f'editrim_delete_{full_token}',
        #         settings.dict_text_for_button['inline_buttons']['all_reminder']: 'list_reminder'
        #     },
        #         max_button_on_row=2
        #     )
        #     await call.message.edit_text(text='Напоминание включено', reply_markup=reply)
        if 'delete' in call_data:
            db.delete_reminder(full_token)
            reply = builers.create_builder_inline(dict_for_button={
                settings.dict_text_for_button['inline_buttons']['restore_reminder']: f'editrim_restore_{full_token}',
                settings.dict_text_for_button['inline_buttons']['all_reminder']: 'list_reminder'
            },
                max_button_on_row=1)
            await call.message.edit_text(text='Напоминание удалено', reply_markup=reply)

        if 'restore' in call_data:
            db.restore_reminder(full_token)
            info_reminder = db.get_info_reminder(full_token)
            msg_info_reminder = f"""{info_reminder['text']}\n\n<b>Время отправки:</b> {info_reminder['date_rim']}"""
            reply = builers.create_builder_inline(dict_for_button={
                settings.dict_text_for_button['inline_buttons']['delete_riminder']: f'editrim_delete_{full_token}',
                settings.dict_text_for_button['inline_buttons']['all_reminder']: 'list_reminder'
            },
                max_button_on_row=1)
            await call.message.edit_text(text=f'Напоминание восстановлено\n{msg_info_reminder}', reply_markup=reply)



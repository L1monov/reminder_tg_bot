import asyncio

from aiogram import Bot
from data.database import My_Database
from datetime import datetime
import asyncio



async def send_message(bot: Bot, tg_id, text):
    msg = f"""📢Напоминание📢
{text}"""
    try:
        await bot.send_message(int(tg_id), text=msg)
    except:
        pass

async def check_for_send(bot: Bot):
    # dict_reminder = db.get_all_reminder_for_send()
    while True:
        db = My_Database()
        dict_reminder = db.get_all_reminder_for_send()
        # Получаем текущее время
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')

        for _ in dict_reminder:
            date_rim = datetime.strptime(dict_reminder[_]['date_rim'], '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M')

            if date_rim == current_time:
                print(dict_reminder[_])
                await send_message(bot=bot, tg_id=dict_reminder[_]['tg_id'], text=dict_reminder[_]['text'])
                db.set_status_reminder(token=dict_reminder[_]['token'], status='shipped')
        await asyncio.sleep(10)





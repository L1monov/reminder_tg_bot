from aiogram import Dispatcher, Bot, Router, F, types
import asyncio
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from handlers import user_commands
from callbacks import callbacks
from cheker_reminders import send_reminder

router = Router()



async def main():
    await asyncio.gather(
        send_reminder.check_for_send(bot),
        run_bot()
    )


async def run_bot():
    bot = Bot(TOKEN,
              parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(
        router,
        user_commands.router,
        callbacks.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    print('Bot rolling')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
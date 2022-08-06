import logging
import config
from filters import IsAdminFilter
from aiogram import Bot, Dispatcher, executor, types


PREFIX = "!+"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
# active filters
dp.filters_factory.bind(IsAdminFilter)

# send_welcome
@dp.message_handler(commands=["hello", "start", "help"], commands_prefix=PREFIX)
async def send_welcome(message:types.Message):
    await message.reply("Нахер ты меня звал, долбаёб?")

# block users(admins only!)
@dp.message_handler(is_admin=True, commands=["block"], commands_prefix=PREFIX)
async def cmd_block(message:types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение, даун...")

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)
    await message.reply_to_message.reply("Пользователь ультра пошел нахуй... Заебал уже...")


# remove "new user joined" messages
@dp.message_handler(content_types=["new_chat_members"])
async def on_user_joined(message:types.Message):
    await message.delete()


# run long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)


from aiogram import Bot, Dispatcher, executor
from aiogram.types.message import Message
import json
import config

bot = Bot(config.bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["need_help", "h"])
async def help_call(message: Message):
    with open("db.json", "r") as f:
        db = json.load(f)
    lstr = ", ".join(
        [
            f'<a href="tg://user?id={applied}">{applied}</a>'
            for applied in db.get("applied")
        ]
    )
    await message.reply(
        text=f"<b>Ваш призыв о помощи был услышан!</b>\n<i>Созванные участники: </i>"
        + lstr,
        parse_mode="HTML",
    )


@dp.message_handler(commands=["apply", "a"])
async def help_call(message: Message):
    with open("db.json", "r") as f:
        db = json.load(f)
    db["applied"].append(message.from_user.id)
    with open("db.json", "w") as f:
        json.dump(db, f)
    await message.reply(
        text=f"<b>Вы успешно добавлены в список помощников.</b>\nТеперь я буду тегать вас, если кто-то напишет команду /need_help или /h",
        parse_mode="HTML",
    )


@dp.message_handler(commands=["unapply", "unap"])
async def help_call(message: Message):
    with open("db.json", "r") as f:
        db = json.load(f)
    db["applied"].remove(message.from_user.id)
    with open("db.json", "w") as f:
        json.dump(db, f)
    await message.reply(
        text=f"<b>Вы успешно удалены из списка помощников.</b>\nЯ больше не буду тегать вас, если кто-то попросит о помощи",
        parse_mode="HTML",
    )


@dp.message_handler(commands=["start"])
async def help_call(message: Message):
    await message.reply(
        text=f"<b>Я - бот, который призван упростить оказание помощи.</b>\nЧтобы бот тегал вас, когда кто-то нуждается в помощи, используйте команду /apply или /a.\nЕсли вы нуждаетесь в помощи, используйте команду /h или /need_help\nСвязь с разработчиком - @fuccq\nSource code: https://github.com/fuccsoc/NeedHelpBot",
        parse_mode="HTML",
        disable_web_page_preview=True
    )


executor.start_polling(dp, skip_updates=True)

import asyncio
from aiogram import Bot, Dispatcher
from exam import r


bot = Bot(token='8522941507:AAGVvmF2uJdNgxjT-UyJPPP3YjDelu1w-lY')
dp = Dispatcher()

dp.include_router(r)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
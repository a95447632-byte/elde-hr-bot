import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from handlers.start import router as start_router
from handlers.resume import router as resume_router
from handlers.admin import router as admin_router
from handlers.resume import router as get_chat_id_router
# 🔥 DB import
from db.models import create_tables
from db.seed import seed_data


async def main():
    os.makedirs("photos", exist_ok=True)

    # 🔥 DB INIT
    print("📦 DB tayyorlanmoqda...")
    create_tables()
    seed_data()
    print("✅ DB tayyor!")

    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Router'lar
    dp.include_router(start_router)
    dp.include_router(resume_router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    print("🚀 Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
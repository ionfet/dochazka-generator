# bot.py
"""
Telegram-бот для генерации Docházka из файла Mzdy.
"""

import os
import re
import shutil
import tempfile
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from generator import generate, DochazkaError

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in .env")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

FILENAME_PATTERN = re.compile(r"^mzdy[_\s]?\d{1,2}[._]\d{4}\.xlsx$", re.IGNORECASE)

HELP_TEXT = (
    "Привет! Отправь мне файл Mzdy и я сгенерирую книгу посещаемости (Docházku).\n\n"
    "Файл должен называться в формате Mzdy_MM.YYYY.xlsx\n"
    "Например: Mzdy_03.2026.xlsx"
)

WRONG_FORMAT_TEXT = (
    "Отправь мне файл Mzdy в формате .xlsx\n\n"
    "Файл должен называться Mzdy_MM.YYYY.xlsx\n"
    "Например: Mzdy_03.2026.xlsx"
)


@dp.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(HELP_TEXT)


@dp.message(F.document)
async def handle_document(message: Message):
    doc = message.document
    filename = doc.file_name or ""

    # Check extension
    if not filename.lower().endswith(".xlsx"):
        await message.answer(WRONG_FORMAT_TEXT)
        return

    # Check filename pattern
    if not FILENAME_PATTERN.match(filename):
        await message.answer(
            "Файл должен называться в формате Mzdy_MM.YYYY.xlsx\n"
            "Например: Mzdy_03.2026.xlsx\n\n"
            "Переименуй файл и отправь снова."
        )
        return

    tmp_dir = tempfile.mkdtemp()
    try:
        # Download
        input_path = os.path.join(tmp_dir, filename)
        file = await bot.get_file(doc.file_id)
        await bot.download_file(file.file_path, input_path)

        # Extract month/year for output filename
        m = re.search(r"(\d{1,2})[._](\d{4})", filename)
        output_name = f"Dochazka_{m.group(1).zfill(2)}.{m.group(2)}.xlsx"
        output_path = os.path.join(tmp_dir, output_name)

        # Generate
        summary = generate(input_path, output_path)

        # Send result
        result_file = FSInputFile(output_path, filename=output_name)
        await message.answer_document(result_file, caption=summary.format_text())

    except DochazkaError as e:
        await message.answer(f"Ошибка: {e}")
    except Exception:
        log.exception("Unexpected error processing document")
        await message.answer(
            "Произошла непредвиденная ошибка. Попробуй ещё раз."
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


@dp.message()
async def handle_other(message: Message):
    await message.answer(WRONG_FORMAT_TEXT)


async def main():
    log.info("Bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

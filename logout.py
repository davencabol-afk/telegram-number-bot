from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import sys

API_ID = 38515912
API_HASH = "835fe2b331b4957172bc432be2566e4b"
SESSION_NAME = "my_session"          # nama session file .session
OWNER_ID = 8231944232                # id telegram kamu
BOT_TOKEN = "8296465888:AAH2VCUzo3_txAG-mez6MDD6-Clg1QkblZQ"  # <--- TEMPAT TOKEN BOT

app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN               # <--- Bot token ditambahkan di sini
)


# command untuk meminta konfirmasi logout
@app.on_message(filters.command("sessions") & filters.user(OWNER_ID))
async def ask_logout(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✔ YA, Logout", callback_data="logout_yes")],
        [InlineKeyboardButton("❌ Batal", callback_data="cancel")]
    ])

    await message.reply(
        "⚠ **Apakah kamu benar-benar ingin logout session ini?**",
        reply_markup=keyboard
    )


# tombol callback
@app.on_callback_query()
async def callback_handler(client, callback_query):
    if callback_query.from_user.id != OWNER_ID:
        return await callback_query.answer("Tidak memiliki izin!")

    if callback_query.data == "logout_yes":
        session_file = f"{SESSION_NAME}.session"

        # kirim file session sebelum dihapus
        if os.path.exists(session_file):
            await callback_query.message.reply_document(
                session_file,
                caption="📦 Ini file session sebelum dihapus."
            )

        await callback_query.edit_message_text("🔒 Session telah dihapus & bot sedang logout...")

        # hapus file session
        if os.path.exists(session_file):
            os.remove(session_file)

        # stop bot & exit
        await app.stop()
        sys.exit()

    if callback_query.data == "cancel":
        await callback_query.edit_message_text("❎ Dibatalkan, session tetap aman.")


app.run()

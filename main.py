    from telethon import TelegramClient,events
import os

# Ganti dengan data kamu
API_ID = 21680958
API_HASH = "1efb3f668181200b37eaaa9a6777d54b"
BOT_TOKEN = "8483722538:AAEQ5PP4jzaF7zk3ZErpQBk3BEpAijdXjBE"

# Inisialisasi bot client
bot = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Tempat menyimpan login user sementara
pending_logins = {}

# --- Handler untuk /start ---
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond(
        "🎉 **Welcome to Robot!**\n\n"
        "Enter your phone number with the country code.\n"
        "Example: `+62xxxxxxxxxx`"
    )
    raise events.StopPropagation


# --- Handler untuk input user ---
@bot.on(events.NewMessage)
async def handler(event):
    user_id = event.sender_id
    text = event.raw_text.strip()

    # Jika user kirim nomor telepon
    if text.startswith('+') and any(c.isdigit() for c in text):
        phone = text
        session_name = f"session_{user_id}"
        client = TelegramClient(session_name, API_ID, API_HASH)
        pending_logins[user_id] = client
        await client.connect()

        try:
            await client.send_code_request(phone)
            await event.respond("📩 Kode OTP sudah dikirim ke Telegram kamu.\nKirim kode itu di sini untuk melanjutkan.")
            pending_logins[user_id] = (client, phone)
        except Exception as e:
            await event.respond(f"❌ Gagal mengirim kode: `{e}`")
        return

    # Jika user kirim kode OTP
    if user_id in pending_logins:
        client, phone = pending_logins[user_id]
        code = text.replace(" ", "")

        try:
            await client.sign_in(phone=phone, code=code)
            await event.respond("✅ Login berhasil! Membuat file session...")

            # Tutup koneksi
            await client.disconnect()

            # Kirim file session ke user
            file_path = f"{client.session.filename}.session"
            await bot.send_file(user_id, file_path, caption="🎉 Ini file session kamu!")

            # Hapus data sementara dan file lokal (opsional)
            del pending_logins[user_id]
            os.remove(file_path)
        except Exception as e:
            await event.respond(f"⚠️ Gagal login: `{e}`")
            del pending_logins[user_id]


print("🤖 Bot sedang berjalan...")
bot.run_until_disconnected()

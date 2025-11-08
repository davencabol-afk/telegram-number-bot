from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import pandas as pd

BOT_TOKEN = "8549273191:AAEKv6drXNJXish65KoOOQ27pyL5zNQtvZI"

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if not document:
        await update.message.reply_text("Kirim file .txt atau .xlsx yang berisi nomor, ya!")
        return

    file = await document.get_file()
    file_name = document.file_name.lower()
    file_path = await file.download_to_drive(custom_path=file_name)

    numbers = []

    try:
        if file_name.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if "," in content:
                numbers = [n.strip() for n in content.split(",") if n.strip()]
            else:
                numbers = [n.strip() for n in content.splitlines() if n.strip()]

        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(file_path, header=None)
            for col in df.columns:
                numbers.extend(df[col].dropna().astype(str).tolist())

        else:
            await update.message.reply_text("Format file tidak didukung 😅 (gunakan .txt atau .xlsx)")
            return

        # Hapus duplikat dan kosong
        unique_numbers = sorted(set(n for n in numbers if n.strip()))

        if not unique_numbers:
            await update.message.reply_text("Tidak ada nomor valid ditemukan 😕")
            return

        formatted = "\n".join([f"{i+1}. {num}" for i, num in enumerate(unique_numbers)])
        await update.message.reply_text(f"Berikut daftar nomor uniknya ({len(unique_numbers)} total):\n\n{formatted}")

    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan saat memproses file: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Kirim file .txt atau .xlsx yang berisi daftar nomor. "
        "Saya akan kirim balik daftar bersihnya tanpa duplikat 📋"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^/start$"), start))

    print("🤖 Bot sedang berjalan...")
    app.run_polling()

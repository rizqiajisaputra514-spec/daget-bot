import re, time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# Ganti pake TOKEN bot kamu dari @BotFather
TOKEN = "8564828970:AAFMTqRMregjGSUUY4m6cqClWh2usQHEmR0" 

# Ganti pake username channel kamu, pake @
CHANNEL_USERNAME = "@Kirim_Daget"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 Pake Username Asli", callback_data='asli')],
        [InlineKeyboardButton("🕵️ Samarkan Nama", callback_data='anon')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Pilih identitas buat kirim daget:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data[user_id] = query.data 
    await query.edit_message_text("Oke, sekarang kirim link DANA Kaget kamu.\n\nContoh: https://link.dana.id/kaget?c=xxx")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.from_user.id
    text = update.message.text

    if user_id not in user_data:
        await update.message.reply_text("Klik /start dulu buat pilih identitas ya.")
        return

    # Cek link dana
    if not re.match(r"https://link\.dana\.id/kaget\?c=[a-zA-Z0-9]+", text):
        await update.message.reply_text("Link DANA Kaget ga valid. Cek lagi ya.")
        return

    mode = user_data[user_id]
    
    if mode == 'asli':
        nama = f"@{update.from_user.username}" if update.from_user.username else update.from_user.full_name
        caption = f"Daget dari {nama} 👇\n\n{text}"
    else: # anon
        caption = f"Daget dari Anonymous 🕵️\n\n{text}"

    try:
        await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=caption)
        await update.message.reply_text("✅ Daget berhasil dikirim ke channel!")
    except Exception as e:
        await update.message.reply_text(f"Gagal kirim ke channel. Pastiin bot udah jadi admin.\nError: {e}")

    del user_data[user_id]

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot jalan...")
    app.run_polling()

if __name__ == '__main__':
    main()

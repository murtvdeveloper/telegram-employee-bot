from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from database import init_db
from auth import is_authorized
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_authorized(user_id):
        await update.message.reply_text(
            "Вы — учредитель или генеральный директор. Доступ разрешен."
        )
    else:
        await update.message.reply_text(
            "Добро пожаловать. Вы можете просматривать только свои данные."
        )

def main():
    token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))

    init_db()

    application.run_polling()

if __name__ == "__main__":
    main()

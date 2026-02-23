import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)

TOKEN = os.getenv("TOKEN")

NAME, ADDRESS = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "——お電話ありがとうございます。\n"
        "警視庁渋谷警察署、刑事課の田中と申します。\n\n"
        "今、少々お時間よろしいでしょうか。\n"
        "ご本人様確認のため、お名前をお伺いしてもよろしいでしょうか。"
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        "ありがとうございます。\nご住所をお願いいたします。"
    )
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.message.text
    await update.message.reply_text(
        "確認が取れました。\n\n"
        "現在、捜査中の案件に関して確認事項がございます。\n"
        "詳細につきましては、担当弁護士よりご連絡いたします。\n\n"
        "本件については第三者への共有をお控えください。\n"
        "ご協力ありがとうございました。"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("キャンセルしました。")
    return ConversationHandler.END


app = ApplicationBuilder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv)

app.run_polling()

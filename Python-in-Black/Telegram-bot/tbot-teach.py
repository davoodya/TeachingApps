from dotenv import load_dotenv
from os import getenv

from subprocess import run, getoutput
from telegram import Update

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Section 1: Commands Functions

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Welcome to your bot.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Available commands: /start, /help, /clipboard ,/echo')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    echo_text = update.message.text
    echo_text = echo_text.split("/echo")
    await update.message.reply_text(update.message.text)

async def non_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Command not Available, See /help for Available Commands.")

async def clpboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clipbrd = run(["powershell.exe", "-NoProfile", "-command", "get-clipboard"],
                  capture_output=True,
                  text=True)
    await update.message.reply_text(f"Cipboard: \n {clipbrd.stdout}")

    # if clipbrd.stderr:
    #     await update.message.reply_text(f"Cipboard: \n {clipbrd.stderr}")
    # else:
    #     await update.message.reply_text(f"Cipboard: \n {clipbrd.stdout}")

async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_cmd = update.message.text
    user_cmd = str(user_cmd).split("/cmd")
    response_cmd = getoutput(user_cmd[1])
    await update.message.reply_text(f"Command Response:\n {response_cmd}")

# Section 2: Connect to Telegram Bot, Register Commands
def main():
    load_dotenv()
    BOT_TOKEN = getenv("TELEGRAM_TOKEN")
    BOT_TOKEN = str(BOT_TOKEN)
    # USER_ID = getenv("TELEGRAM_USER_ID")

    # Connect Python Script to Telegram Bot
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("clipboard", clpboard))
    application.add_handler(CommandHandler("cmd", cmd))

    # Response Non-Command Messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, non_cmd))

    # Run Polling(Bot)
    application.run_polling()

if __name__ == "__main__":
    print("Telegram Bot Running...")
    main()

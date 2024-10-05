# Advanced Telegram Music Bot

import os
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from youtube_dl import YoutubeDL

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a command handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()}! Use /play <song_name> to play music.",
        reply_markup=ForceReply(selective=True),
    )

# Define a command handler for the /play command
def play(update: Update, context: CallbackContext) -> None:
    if context.args:
        song_name = ' '.join(context.args)
        update.message.reply_text(f"Searching for {song_name}...")
        download_song(song_name, update)
    else:
        update.message.reply_text("Please provide a song name.")

# Function to download the song using youtube_dl
def download_song(song_name: str, update: Update) -> None:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'type': 'audio/mp3',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
        title = info['entries'][0]['title']
        update.message.reply_text(f"Now playing: {title}")
        update.message.reply_audio(audio=open(f"{title}.mp3", 'rb'))

# Define the main function to run the bot
def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("play", play))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
  

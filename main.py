import os
import pytube
from pyrogram import Client, filters
from dotenv import load_dotenv
from pyrogram.types import Message

if os.path.isfile("config.env"):
    load_dotenv("config.env")

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Pyrogram client
app = Client(name="app", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# define a handler function for messages that contain the "/dlyt" command
@ app.on_message(filters.command("dlyt"))
async def ask_for_format(client: Client, message: Message):
    # check if the user provided a YouTube link
    if len(message.command) < 2:
        message.reply_text("Please provide a valid YouTube link after the command.")
        return
    url = message.command[1]
    
    # create a PyTube YouTube object for the video
    try:
        video = pytube.YouTube(url)
    except:
        message.reply_text("Error: Invalid YouTube link.")
        return
    
    # ask the user whether they want to download a video or an audio file
    keyboard = [
        [{"text": "Video (MP4)", "callback_data": "video_mp4"}],
        [{"text": "Audio (MP3)", "callback_data": "audio_mp3"}],
    ]
    reply_markup = {
        "inline_keyboard": keyboard
    }
    message.reply_text("What format would you like to download?", reply_markup=reply_markup)
    
    # store the YouTube URL in a dictionary so we can use it later
    client.storage.set("current_url", url)

# define a handler function for callback queries from the download format keyboard
@ app.on_callback_query()
async def handle_callback_query(client: Client, query: CallbackQuery):
    # get the current YouTube URL from storage
    url = client.storage.get("current_url")
    
    # get the desired download format from the callback data
    format = query.data.split("_")[0]
    
    # create a PyTube YouTube object for the video
    video = pytube.YouTube(url)
    
    # download the video or audio file in the desired format
    if format == "video":
        # download the highest resolution MP4 video
        stream = video.streams.get_highest_resolution()
        stream.download()
        message.reply_text("Video downloaded successfully.")
    elif format == "audio":
        # download the audio file as an MP3
        stream = video.streams.filter(only_audio=True).first()
        stream.download()
        message.reply_text("Audio downloaded successfully.")
    else:
        message.reply_text("Error: Invalid download format.")

# define a handler function for messages that contain the "/start" command
@ app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    message.reply_text("Hi!!! I'm alive.")

# run the Pyrogram client
app.run()

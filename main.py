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

# define a handler function for messages that contain a YouTube link
@ app.on_message(filters.regex(r"(http(s)?://)?((w){3}.)?youtu(be|.be)?(\.com)?/.+"))
async def download_media(client: Client, message: Message):
    # extract the YouTube video URL from the message text
    url = message.text
    
    # create a PyTube YouTube object for the video
    video = pytube.YouTube(url)
    
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
    # get the YouTube URL from the storage dictionary
    url = client.storage.get("current_url")
    
    # extract the requested format from the callback data
    callback_data = query.data
    format_type, format_extension = callback_data.split("_")
    
    # create a PyTube YouTube object for the video
    video = pytube.YouTube(url)
    
    if format_type == "video":
        # get the highest resolution video stream
        stream = video.streams.get_highest_resolution()
        
        # download the video to a file in the current directory
        stream.download(filename="video.mp4")
        
        # send the downloaded video file as a reply to the original message
        client.send_video(
            chat_id=query.message.chat.id,
            video="video.mp4",
            reply_to_message_id=query.message.reply_to_message.message_id
        )
        
        # delete the downloaded video file from the local filesystem
        os.remove("video.mp4")
    
    elif format_type == "audio":
        # get the highest bitrate audio stream
        stream = video.streams.get_audio_only().order_by("bitrate").desc().first()
        
        # download the audio to a file in the current directory
        stream.download(filename="audio." + format_extension)
        
        # send the downloaded audio file as a reply to the original message
        client.send_audio(
            chat_id=query.message.chat.id,
            audio="audio." + format_extension,
            reply_to_message_id=query.message.reply_to_message.message_id
        )
        
        # delete the downloaded audio file from the local filesystem
        os.remove("audio." + format_extension)

# start the Pyrogram client
app.run()


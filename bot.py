import os
import asyncio
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً فيك 🔥\n\nابعتلي رابط فيديو من يوتيوب / تيك توك / انستا\nوأنا بحملو وببعتلك ياه"
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "http" not in url:
        await update.message.reply_text("ابعت رابط صحيح، مو رسالة عادية 🙏")
        return

    msg = await update.message.reply_text("عم حمل... استنى شوي ⏳")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(
            video=open(filename, 'rb'),
            caption=f"تم ✅\n{info.get('title', '')}"
        )
        await msg.delete()
        os.remove(filename)

    except Exception as e:
        await msg.edit_text(f"ما قدرت حمل هاد الرابط 😢\nجرب رابط تاني")
        print(e)

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    print("Bot started")
    app.run_polling()

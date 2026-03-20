import threading
import yt_dlp
import os

# הגדרת נתיב התיקייה החדשה
ELAZAR_PATH = "/storage/emulated/0/Download/ELAZAR_DOWNLOADS/"

def download_video(url, fmt, progress_cb, done_cb, error_cb):
    def run():
        try:
            # יצירת התיקייה אם היא לא קיימת
            if not os.path.exists(ELAZAR_PATH):
                os.makedirs(ELAZAR_PATH)

            ydl_format = "bestaudio/best" if "MP3" in fmt else "best"

            def hook(d):
                if d['status'] == 'downloading':
                    p = d.get('downloaded_bytes', 0)
                    t = d.get('total_bytes', 1) or d.get('total_bytes_estimate', 1)
                    progress_cb((p / t) * 100)
                elif d['status'] == 'finished':
                    progress_cb(100)

            ydl_opts = {
                'format': ydl_format,
                'outtmpl': os.path.join(ELAZAR_PATH, '%(title)s.%(ext)s'),
                'progress_hooks': [hook],
                'noplaylist': True,
                'restrictfilenames': True,
            }

            if "MP3" in fmt:
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            done_cb()
        except Exception as e:
            error_cb(str(e))

    threading.Thread(target=run, daemon=True).start()

import threading
import yt_dlp
import os

# הגדרת נתיב התיקייה
ELAZAR_PATH = "/storage/emulated/0/Download/ELAZAR_DOWNLOADS/"

# מחלקה שמונעת את שגיאת ה-'write' באנדרואיד
class MyLogger:
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

def download_video(url, fmt, progress_cb, done_cb, error_cb):
    def run():
        try:
            # יצירת התיקייה אם היא לא קיימת
            if not os.path.exists(ELAZAR_PATH):
                os.makedirs(ELAZAR_PATH, exist_ok=True)

            def hook(d):
                if d['status'] == 'downloading':
                    p = d.get('downloaded_bytes', 0)
                    t = d.get('total_bytes', 1) or d.get('total_bytes_estimate', 1)
                    progress_cb((p / t) * 100)
                elif d['status'] == 'finished':
                    progress_cb(100)

            # הגדרות yt-dlp עם ה-logger המתוקן
            ydl_opts = {
                'format': 'bestaudio/best' if "MP3" in fmt else 'best',
                'outtmpl': os.path.join(ELAZAR_PATH, '%(title)s.%(ext)s'),
                'progress_hooks': [hook],
                'noplaylist': True,
                'logger': MyLogger(),  # זה התיקון הקריטי!
                'verbose': False,
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

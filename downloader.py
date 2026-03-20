import threading
import yt_dlp
import os

ELAZAR_PATH = "/storage/emulated/0/Download/ELAZAR_DOWNLOADS/"

def download_video(url, fmt, progress_cb, done_cb, error_cb):
    def run():
        try:
            if not os.path.exists(ELAZAR_PATH):
                os.makedirs(ELAZAR_PATH)

            def hook(d):
                if d['status'] == 'downloading':
                    p = d.get('downloaded_bytes', 0)
                    t = d.get('total_bytes', 1) or d.get('total_bytes_estimate', 1)
                    progress_cb((p / t) * 100)
                elif d['status'] == 'finished':
                    progress_cb(100)

            ydl_opts = {
                'format': 'bestaudio/best' if fmt == "MP3" else 'best',
                'outtmpl': os.path.join(ELAZAR_PATH, '%(title)s.%(ext)s'),
                'progress_hooks': [hook],
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            done_cb()
        except Exception as e:
            error_cb(str(e))

    threading.Thread(target=run, daemon=True).start()

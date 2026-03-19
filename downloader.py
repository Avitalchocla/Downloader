import threading
import yt_dlp

DOWNLOAD_PATH = "/storage/emulated/0/Download/"

def download_video(url, fmt, quality, progress_cb, done_cb, error_cb):

    def run():
        try:
            if fmt == "MP3":
                ydl_format = "bestaudio/best"
            else:
                if quality == "Best":
                    ydl_format = "best"
                elif quality == "1080p":
                    ydl_format = "bestvideo[height<=1080]+bestaudio/best"
                elif quality == "720p":
                    ydl_format = "bestvideo[height<=720]+bestaudio/best"
                else:
                    ydl_format = "bestvideo[height<=480]+bestaudio/best"

            def hook(d):
                if d['status'] == 'downloading':
                    percent = d.get('_percent_str', '0%').replace('%','')
                    try:
                        progress_cb(float(percent))
                    except:
                        pass
                elif d['status'] == 'finished':
                    progress_cb(100)

            ydl_opts = {
                'format': ydl_format,
                'outtmpl': DOWNLOAD_PATH + '%(title)s.%(ext)s',
                'progress_hooks': [hook],
                'noplaylist': True,
            }

            if fmt == "MP3":
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
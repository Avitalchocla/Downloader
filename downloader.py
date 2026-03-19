import threading
import yt_dlp
import os
import re

DOWNLOAD_PATH = "/storage/emulated/0/Download/"

# פונקציית עזר לניקוי שם הקובץ מתווים בעייתיים
def clean_filename(title):
    # מסיר תווים לא חוקיים בשמות קבצים (כמו ?, |, \, / וכו')
    return re.sub(r'[\\/*?:"<>|]', "", title)

def download_video(url, fmt, quality, progress_cb, done_cb, error_cb):
    def run():
        try:
            # הגדרת פורמט ההורדה לפי הבחירה
            if fmt == "MP3 (Audio)":
                ydl_format = "bestaudio/best"
            else:
                ydl_format = "best"

            # פונקציה פנימית לעדכון ההתקדמות (Progress Hook)
            def hook(d):
                if d['status'] == 'downloading':
                    try:
                        p = d.get('downloaded_bytes', 0)
                        t = d.get('total_bytes', 1)
                        if t == 1:
                            t = d.get('total_bytes_estimate', 1)
                        percent = (p / t) * 100
                        # וידוא שהאחוז נשאר בין 0 ל-100
                        percent = max(0, min(100, percent))
                        progress_cb(percent)
                    except:
                        pass
                elif d['status'] == 'finished':
                    progress_cb(100)

            # הגדרת אופציות ל-YoutubeDL
            ydl_opts = {
                'format': ydl_format,
                # מבנה שם הקובץ: תיקיית ההורדות / שם הסרטון.סיומת
                'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
                'progress_hooks': [hook],
                'noplaylist': True,  # הורדת סרטון בודד, לא פלייליסט
                'quiet': True,
                'no_warnings': True,
                # ניקוי אוטומטי של שמות קבצים בעברית או תווים מוזרים
                'restrictfilenames': True,
            }

            # הגדרות מיוחדות להמרת MP3
            if fmt == "MP3 (Audio)":
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',  # איכות שמע טובה
                }]

            # הפעלת ההורדה
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            done_cb()
        except Exception as e:
            # תפיסת כל שגיאה והעברתה ל-UI
            error_cb(str(e))

    # הרצת ההורדה ב-thread נפרד כדי לא לתקוע את האפליקציה
    threading.Thread(target=run, daemon=True).start()

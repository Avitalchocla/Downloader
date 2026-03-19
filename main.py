from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.clipboard import Clipboard  # הוספנו קליפבורד
from downloader import download_video

# פונקציה לבקשת הרשאות באנדרואיד
def ask_android_permissions():
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE
        ])

class ElazarApp(App):  # שינינו את שם המחלקה
    def build(self):
        self.title = "ELAZAR"  # הגדרת שם האפליקציה
        # בקשת הרשאות מיד עם עליית האפליקציה
        ask_android_permissions()
        return Builder.load_file("ui.kv")

    def paste_link(self):
        # פונקציה שמדביקה את הקישור מהקליפבורד
        clipboard_data = Clipboard.paste()
        if clipboard_data:
            self.root.ids.url_input.text = clipboard_data
            self.update_status("✅ Link pasted from clipboard")
        else:
            self.update_status("❌ Clipboard is empty")

    def start_download(self):
        url = self.root.ids.url_input.text.strip()
        if not url:
            self.update_status("❌ No link provided")
            return

        self.update_status("🔄 Checking and Starting...")
        self.root.ids.progress.value = 0

        # קריאה לפונקציית ההורדה עם callbacks
        download_video(
            url,
            self.root.ids.format_spinner.text,
            self.root.ids.quality_spinner.text,
            self.progress_callback,
            self.finish_callback,
            self.error_callback
        )

    def progress_callback(self, percent):
        Clock.schedule_once(lambda dt: self.set_progress(percent))

    def finish_callback(self, filename="file"):
        Clock.schedule_once(lambda dt: self.update_status(f"✅ Success: Check Downloads folder"))

    def error_callback(self, error):
        Clock.schedule_once(lambda dt: self.update_status(f"❌ Error: {error}"))

    def set_progress(self, value):
        self.root.ids.progress.value = value
        self.root.ids.status.text = f"Downloading: {int(value)}%"

    def update_status(self, text):
        self.root.ids.status.text = text

if __name__ == "__main__":
    ElazarApp().run()

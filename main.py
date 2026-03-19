from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from downloader import download_video

def ask_android_permissions():
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

class MainApp(App):
    def build(self):
        ask_android_permissions()
        return Builder.load_file("ui.kv")

    def start_download(self):
        url = self.root.ids.url_input.text.strip()
        if not url:
            self.update_status("❌ אין קישור")
            return
        self.update_status("🔄 מתחיל...")
        download_video(url, self.root.ids.format_spinner.text, self.root.ids.quality_spinner.text, self.progress_callback, self.finish_callback, self.error_callback)

    def progress_callback(self, percent):
        Clock.schedule_once(lambda dt: self.set_progress(percent))

    def finish_callback(self):
        Clock.schedule_once(lambda dt: self.update_status("✅ הושלם!"))

    def error_callback(self, error):
        Clock.schedule_once(lambda dt: self.update_status(f"שגיאה: {error}"))

    def set_progress(self, value):
        self.root.ids.progress.value = value
        self.root.ids.status.text = f"{int(value)}%"

    def update_status(self, text):
        self.root.ids.status.text = text

if __name__ == "__main__":
    MainApp().run()
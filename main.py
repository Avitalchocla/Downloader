from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.clipboard import Clipboard
import os
from downloader import download_video, ELAZAR_PATH

class ElazarApp(App):
    def build(self):
        self.title = "ELAZAR"
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.INTERNET
            ])
        return Builder.load_file("ui.kv")

    def paste_link(self):
        text = Clipboard.paste()
        if text:
            self.root.ids.url_input.text = text
            self.update_status("✅ Link Pasted")

    def start_download(self):
        url = self.root.ids.url_input.text.strip()
        if not url:
            self.update_status("❌ Paste a link first")
            return
        
        self.update_status("🔄 Starting Download...")
        self.root.ids.progress.value = 0
        
        download_video(
            url, 
            self.root.ids.format_spinner.text,
            self.progress_callback, 
            self.finish_callback, 
            self.error_callback
        )

    def progress_callback(self, percent):
        Clock.schedule_once(lambda dt: self.set_progress(percent))

    def finish_callback(self):
        Clock.schedule_once(lambda dt: self.update_status("✅ Saved to ELAZAR_DOWNLOADS"))

    def error_callback(self, error):
        Clock.schedule_once(lambda dt: self.update_status(f"❌ Error: {error}"))

    def set_progress(self, value):
        self.root.ids.progress.value = value
        self.root.ids.status.text = f"Progress: {int(value)}%"

    def update_status(self, text):
        self.root.ids.status.text = text

if __name__ == "__main__":
    ElazarApp().run()

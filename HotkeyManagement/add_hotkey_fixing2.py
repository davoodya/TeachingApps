import keyboard
from threading import Thread, Event
import time

class HotkeyManager:
    def __init__(self):
        self.exit_event = Event()
        self.hotkeys = [
            ('ctrl+alt+c', self.send_clipboard),
            ('ctrl+alt+y', lambda: self.send_text(self.send_clipboard))
        ]
        self.registered_ids = []

    def start(self):
        """ثبت هوتکی‌ها و شروع سیستم"""
        # حذف هوتکی‌های قبلی
        self._cleanup()

        # ثبت هوتکی‌های جدید
        for hotkey, callback in self.hotkeys:
            hotkey_id = keyboard.add_hotkey(hotkey, callback)
            self.registered_ids.append(hotkey_id)

        # شروع ترد گوش دهنده
        Thread(target=self._listener_thread, daemon=True).start()

    def _cleanup(self):
        """پاکسازی هوتکی‌های قبلی"""
        for hotkey_id in self.registered_ids:
            try:
                keyboard.remove_hotkey(hotkey_id)
            except:
                pass
        self.registered_ids.clear()

    def _listener_thread(self):
        """ترد اصلی برای نگه داشتن برنامه"""
        while not self.exit_event.is_set():
            keyboard.wait()
            time.sleep(0.1)  # جلوگیری از مصرف CPU بالا

    def stop(self):
        """توقف سیستم"""
        self.exit_event.set()
        self._cleanup()

# استفاده نمونه:
if __name__ == "__main__":
    manager = HotkeyManager()
    manager.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.stop()
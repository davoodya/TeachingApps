import keyboard
from threading import Thread, Lock
import time

class HotkeySystem:
    def __init__(self):
        self.lock = Lock()
        self.active = True
        self.hotkeys = {
            'ctrl+alt+c': self.send_clipboard,
            'ctrl+alt+y': lambda: self.send_text(self.send_clipboard)
        }

    def start(self):
        """راه‌اندازی سیستم با ترد جداگانه"""
        Thread(target=self._run, daemon=True).start()

    def _run(self):
        """ترد اصلی برای مدیریت هوتکی‌ها"""
        while self.active:
            with self.lock:
                # پاکسازی قبل از ثبت جدید
                keyboard.unhook_all_hotkeys()

                # ثبت هوتکی‌ها
                for combo, callback in self.hotkeys.items():
                    keyboard.add_hotkey(combo, callback)

            # تأخیر برای کاهش بار CPU
            keyboard.wait()
            time.sleep(0.1)

    def stop(self):
        """توقف سیستم"""
        self.active = False
        keyboard.unhook_all_hotkeys()

# استفاده:
system = HotkeySystem()
system.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    system.stop()
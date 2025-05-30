import keyboard
import time
import sys

def save_file():
    print("💾 File Saved.")

def show_info(name, age):
    print(f"👤 User Info:\n Name={name}, Age={age}")

def exit_app():
    print("❌ App Closed.")
    keyboard.unhook_all_hotkeys()
    raise KeyboardInterrupt

keyboard.add_hotkey('ctrl+alt+s', save_file)
keyboard.add_hotkey('ctrl+shift+i', lambda: show_info("Davood", 28))
keyboard.add_hotkey('ctrl+alt+q', exit_app)

print("🔥 Active Hotkeys:")
print("- Ctrl+Alt+S: Save File")
print("- Ctrl+Shift+I: Show User Info ")
print("- Ctrl+Alt+Q: Quit Applications")


try:
    print("\n Listening to Hotkeys...")
    keyboard.wait()
except KeyboardInterrupt:
    print("Goodbye")
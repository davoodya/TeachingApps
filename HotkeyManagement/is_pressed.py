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
    sys.exit()

def hotkey_monitor():
    if keyboard.is_pressed('ctrl+alt+s'):
        save_file()

    if keyboard.is_pressed('ctrl+shift+i'):
        show_info("Davood", 28)

    if keyboard.is_pressed('ctrl+alt+q'):
        exit_app()

print("🔥 Active Hotkeys:")
print("- Ctrl+Alt+S: Save File")
print("- Ctrl+Shift+I: Show User Info ")
print("- Ctrl+Alt+Q: Quit Applications")

while True:
    hotkey_monitor()
    time.sleep(0.1)

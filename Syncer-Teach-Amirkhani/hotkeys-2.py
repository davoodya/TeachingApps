import keyboard, time

def save_file():
    print("CTRL+ALT+F2 Pressed:\n")
    print("File Saved.")

def show_info(name, age):
    print("CTRL+ALT+F3 Pressed:\n")
    print(f"User Info:\n Name: {name}, Age: {age}")

def exit_app():
    print("Clear all Hotkeys and app closed")
    print("App Closed.")
    keyboard.unhook_all_hotkeys()
    exit()

# Register Hotkeys to run Functions
try:
    keyboard.add_hotkey('ctrl+alt+f2', save_file)
    keyboard.add_hotkey('ctrl+alt+f3', lambda: show_info("Davood", 30))

    # Print Help
    print("""Active Hotkeys:
    - CTRL+ALT+F2 => save file
    - CTRL+ALT+F3 => show info
    - CTRL+ALT+Q => exit app
    
    Listening to Hotkeys...
    
    """)
    keyboard.wait()

except KeyboardInterrupt:
    exit_app()

finally:
    keyboard.unhook_all_hotkeys()


#
# while True:
#     try:
#         time.sleep(1)
#     except KeyboardInterrupt:
#         print("App Closed.")
#         break
#
#

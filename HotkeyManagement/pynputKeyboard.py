from pynput import keyboard, mouse
import threading

# Step 0: Define Hotkey Manager Class
class HotkeyManager:
    # Step 1: Define Hotkey Manager Constructor and Combinations
    def __init__(self):
        self.combinations  = {
            frozenset([keyboard.Key.ctrl_l, keyboard.KeyCode.from_char('\x13')]): #\x13 is the key for "s"
                self.save_file,
            frozenset([keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.KeyCode.from_char('\t')]): #'\t' is the key for "i"
                lambda: self.show_info("Davood", 28),
            frozenset([keyboard.Key.esc]):
                self.exit_app,
        }
        self.current_keys = set()
        self.listener = None

    # Step 2: Define Start(main runner) Function
    def start(self):
        print("🔥 Active Hotkeys:")
        print("- Ctrl+S: Save File")
        print("- Ctrl+Shift+I: Show User Info ")
        print("- Escape: Quit Applications")

        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.listener = listener
            listener.join()

    # Step 3: Define on_press Function
    def on_press(self, key):
        # When a key is pressed, add it to the current_keys set
        self.current_keys.add(key)

        for comb, action in self.combinations.items():
            # If all keys in current_keys are in the combination, then call the action
            if comb.issubset(self.current_keys):
                threading.Thread(target=action).start()
                break

    # Step 4: Define on_release Function
    def on_release(self, key):
        # When a key is released, remove it from the current_keys set
        try:
            self.current_keys.remove(key)
        except KeyError:
            pass


    # Step 5: Define Operative Functions
    def save_file(self):
        print("💾 File Saved.")

    def show_info(self, name, age):
        print(f"👤 User Info:\n Name={name}, Age={age}")

    def exit_app(self):
        print("❌ App Closed.")
        self.listener.stop()

# Step 6: Run the Hotkey Manager
if __name__ == "__main__":
    manager = HotkeyManager()
    manager.start()
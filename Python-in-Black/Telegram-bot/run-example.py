from subprocess import run

output = run(
    ["powershell", "-NoProfile", "-command", f"Set-Clipboard -Value '{text}'"],
    capture_output=True,
    text=True
)

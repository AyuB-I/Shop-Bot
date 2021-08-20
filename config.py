import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
HOST = "localhost"


I18N_DOMAIN = "ShopBot"
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR/"locales"

import os
import logging
from web3 import Web3
from dotenv import load_dotenv
from telegram import Bot

# ------------------- تنظیمات لاگ -------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------- بارگذاری env -------------------
load_dotenv()

BSC_NODE_URL = os.getenv("BSC_NODE_URL")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # آیدی چت خودت

bot = Bot(token=TELEGRAM_TOKEN)

if not BSC_NODE_URL:
    logger.error("❌ آدرس نود BSC در .env تعریف نشده!")
    bot.send_message(chat_id=CHAT_ID, text="❌ آدرس نود BSC در .env تعریف نشده!")
    exit()

# ------------------- تشخیص نوع اتصال -------------------
if BSC_NODE_URL.startswith("wss://"):
    logger.info("🔌 اتصال از طریق WebSocket...")
    w3 = Web3(Web3.WebsocketProvider(BSC_NODE_URL))
else:
    logger.info("🔌 اتصال از طریق HTTP...")
    w3 = Web3(Web3.HTTPProvider(BSC_NODE_URL))

# ------------------- تست اتصال -------------------
try:
    if w3.is_connected():
        net_id = w3.eth.chain_id
        msg = f"✅ اتصال به BSC برقرار شد!\nChain ID: {net_id}"
        logger.info(msg)
        bot.send_message(chat_id=CHAT_ID, text=msg)
    else:
        msg = "❌ اتصال به BSC برقرار نشد!"
        logger.error(msg)
        bot.send_message(chat_id=CHAT_ID, text=msg)
        exit()
except Exception as e:
    err_msg = f"❌ خطا در اتصال: {e}"
    logger.exception(err_msg)
    bot.send_message(chat_id=CHAT_ID, text=err_msg)
    exit()

# ------------------- ادامه کد ربات پامپ‌یاب -------------------
# اینجا کدهای مانیتور کردن تراکنش‌ها و منطق رباتت رو می‌ذاری

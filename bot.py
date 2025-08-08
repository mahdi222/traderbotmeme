import asyncio
import logging
import os
from web3 import Web3
from telegram import Bot
from telegram.constants import ParseMode

# -------------------- تنظیمات --------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # توکن ربات
CHAT_ID = os.getenv("CHAT_ID")  # آیدی چت یا گروه
BSC_NODE_URL = os.getenv("BSC_NODE_URL")  # لینک RPC از NodeReal یا هر نود BSC

# آدرس فکتوری PancakeSwap (ورژن 2)
FACTORY_ADDRESS = Web3.to_checksum_address("0xCA143Ce32Fe78f1f7019d7d551a6402fC5350c73")

# ABI مینیمال برای PairCreated
FACTORY_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "token0", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "token1", "type": "address"},
            {"indexed": False, "internalType": "address", "name": "pair", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "name": "PairCreated",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "allPairsLength",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "allPairs",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# -------------------- تنظیمات لاگ --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- اتصال به BSC --------------------
w3 = Web3(Web3.HTTPProvider(BSC_NODE_URL))
if not w3.is_connected():
    logger.error("❌ اتصال به BSC برقرار نشد!")
    exit(1)
else:
    logger.info("✅ به BSC متصل شدیم")

factory = w3.eth.contract(address=FACTORY_ADDRESS, abi=FACTORY_ABI)
bot = Bot(token=TELEGRAM_TOKEN)


# -------------------- ارسال پیام --------------------
async def send_message(text):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"خطا در ارسال پیام: {e}")


# -------------------- گوش دادن به رویدادها --------------------
async def watch_new_pairs():
    logger.info("👀 شروع مانیتورینگ جفت‌ارزهای جدید...")
    event_filter = factory.events.PairCreated.create_filter(fromBlock="latest")

    while True:
        try:
            for event in event_filter.get_new_entries():
                token0 = event["args"]["token0"]
                token1 = event["args"]["token1"]
                pair = event["args"]["pair"]

                msg = f"🚀 <b>جفت‌ارز جدید پیدا شد!</b>\n\n" \
                      f"Token0: <code>{token0}</code>\n" \
                      f"Token1: <code>{token1}</code>\n" \
                      f"Pair: <code>{pair}</code>"

                logger.info(msg)
                await send_message(msg)

        except Exception as e:
            logger.error(f"خطا در خواندن رویداد: {e}")

        await asyncio.sleep(3)


# -------------------- اجرای برنامه --------------------
async def main():
    await send_message("✅ ربات پامپ‌یاب روشن شد و منتظر جفت‌ارزهای جدید است...")
    await watch_new_pairs()


if __name__ == "__main__":
    asyncio.run(main())

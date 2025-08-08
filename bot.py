import os
import asyncio
import aiohttp
from web3 import Web3
from telegram import Bot

# ---------------------------
# تنظیمات
# ---------------------------
TELEGRAM_TOKEN = "8296961071:AAEWjoANG7T00w0-svmSyIVM4vSosOjgdB4"
ALLOWED_USERS = [610160171]  # فقط آی‌دی‌های مجاز
NODE_REAL_API_KEY = "02f153a065884f34877fbbbe2a474abf"

FACTORY_ADDRESS = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"  # UniswapV2 مثال
FACTORY_ABI = [...]  # اینجا ABI کامل رو بگذار

# ---------------------------
# اتصال Web3 به نود
# ---------------------------
w3 = Web3(Web3.HTTPProvider(f"https://bsc-mainnet.nodereal.io/v1/{NODE_REAL_API_KEY}"))
if not w3.is_connected():
    raise Exception("❌ اتصال به نود برقرار نشد!")

factory = w3.eth.contract(
    address=w3.to_checksum_address(FACTORY_ADDRESS),
    abi=FACTORY_ABI
)

bot = Bot(token=TELEGRAM_TOKEN)

# ---------------------------
# ارسال پیام به کاربران مجاز
# ---------------------------
async def send_message_to_allowed(text):
    for user_id in ALLOWED_USERS:
        try:
            await bot.send_message(chat_id=user_id, text=text)
        except Exception as e:
            print(f"خطا در ارسال پیام به {user_id}: {e}")

# ---------------------------
# شبیه‌ساز تحلیل پامپ (نسخه تست)
# ---------------------------
async def detect_pump_test():
    await asyncio.sleep(5)  # تأخیر برای تست
    coin_name = "TESTCOIN"
    buy_time = "الان"
    sell_time = "۵ دقیقه بعد"
    contract = "0x1234567890abcdef..."
    exchange = "PancakeSwap"

    message = f"""
🚀 سیگنال پامپ شناسایی شد!
💰 اسم ارز: {coin_name}
🕒 زمان خرید: {buy_time}
🕒 زمان فروش: {sell_time}
📜 آدرس کانترکت: {contract}
🏦 صرافی: {exchange}
"""
    await send_message_to_allowed(message)

# ---------------------------
# اجرای اصلی
# ---------------------------
async def main():
    await send_message_to_allowed("✅ ربات تست پامپ‌یاب فعال شد!")
    await detect_pump_test()

if __name__ == "__main__":
    asyncio.run(main())

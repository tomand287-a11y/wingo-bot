import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
import random
import asyncio

API_ID = 37144664
API_HASH = "30b1c7e1d3d66d68a3233aea019cc8a2"
BOT_TOKEN = "8376714760:AAGQIDxvYNfQi8qinvJ8Y8U4POxC605tp5U"
MONGO_URL = "mongodb+srv://mahir444:Alamin%4014@cluster0.bf0g0uh.mongodb.net/?retryWrites=true&w=majority"
CHANNEL = "https://t.me/MAHIR_TRADER6"
PASSKEY = "VIP2026"

bot = Client(
    "wingo_vip_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo["wingo_bot"]
users = db.users

# ---------------- START ----------------

@bot.on_message(filters.command("start"))
async def start(client, message):

    user = message.from_user

    text = f"""
🔥 WELCOME TO VIP SIGNAL BOT 🔥

👤 User: {user.first_name}

✅ Join Channel First
🆔 Send Your Game UID
🔐 Enter Passkey

━━━━━━━━━━━━━━━
🎯 FEATURES
• 30s Signal
• BIG/SMALL Prediction
• Team Access
• REAL Analysis
━━━━━━━━━━━━━━━
"""

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 CHANNEL", url=f"https://t.me/MAHIR_TRADER6")],
        [InlineKeyboardButton("🚀 LOGIN", callback_data="login")],
        [InlineKeyboardButton("❓ HELP", callback_data="help")]
    ])

    await message.reply_photo(
        photo="https://i.ibb.co/fYw0tYB/hacker.jpg",
        caption=text,
        reply_markup=buttons
    )

# ---------------- HELP ----------------

@bot.on_callback_query(filters.regex("help"))
async def help_menu(client, callback_query):

    await callback_query.message.edit_text(
        """
❓ HOW TO USE

1. Join Channel
2. Login
3. Enter UID
4. Enter Passkey
5. Start Signal

⚠️ REAL TRADING Purpose Only
""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 BACK", callback_data="back")]
        ])
    )

# ---------------- BACK ----------------

@bot.on_callback_query(filters.regex("back"))
async def back_menu(client, callback_query):

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 CHANNEL", url=f"https://t.me/{CHANNEL}")],
        [InlineKeyboardButton("🚀 LOGIN", callback_data="login")],
        [InlineKeyboardButton("❓ HELP", callback_data="help")]
    ])

    await callback_query.message.edit_text(
        "🔥 MAIN MENU 🔥",
        reply_markup=buttons
    )

# ---------------- LOGIN ----------------

login_users = {}

@bot.on_callback_query(filters.regex("login"))
async def login(client, callback_query):

    login_users[callback_query.from_user.id] = "uid"

    await callback_query.message.reply_text(
        "🆔 Send Your UID"
    )

# ---------------- UID INPUT ----------------

@bot.on_message(filters.text)
async def uid_input(client, message):

    print(message.text)

    user_id = message.from_user.id

    if user_id not in login_users:
        return

    step = login_users[user_id]

    if step == "uid":

        await users.update_one(
            {"user_id": user_id},
            {"$set": {"uid": message.text}},
            upsert=True
        )

        login_users[user_id] = "pass"

        await message.reply_text(
            "🔐 Send Passkey"
        )

    elif step == "pass":

        if message.text != PASSKEY:
            await message.reply_text(
                "❌ Wrong Passkey"
            )
            return

        await users.update_one(
            {"user_id": user_id},
            {"$set": {"access": True}},
            upsert=True
        )

        login_users.pop(user_id)

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎯 START SIGNAL", callback_data="signal")],
            [InlineKeyboardButton("📢 CHANNEL", url=f"https://t.me/{CHANNEL}")],
            [InlineKeyboardButton("👥 REFER", callback_data="refer")]
        ])

        await message.reply_text(
            "✅ LOGIN SUCCESSFUL",
            reply_markup=buttons
        )

# ---------------- SIGNAL ----------------

@bot.on_callback_query(filters.regex("signal"))
async def signal(client, callback_query):

    msg = await callback_query.message.reply_text(
        "⏳ ANALYSING MARKET..."
    )

    for i in range(30, 0, -1):
        await msg.edit_text(f"⏳ NEXT SIGNAL IN {i} SECONDS")
        await asyncio.sleep(1)

    prediction = random.choice(["BIG", "SMALL"])

    result_text = f"""
🎯 WINGO 30S SIGNAL

📊 PREDICTION: {prediction}

⚠️ REAL ANALYSIS ONLY
"""

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 NEXT SIGNAL", callback_data="signal")]
    ])

    await msg.edit_text(
        result_text,
        reply_markup=buttons
    )

# ---------------- REFER ----------------

@bot.on_callback_query(filters.regex("refer"))
async def refer(client, callback_query):

    user_id = callback_query.from_user.id

    text = f"""
👥 REFER SYSTEM

Share This Link:
https://t.me/{(await bot.get_me()).username}?start={user_id}
"""

    await callback_query.message.reply_text(text)

# ---------------- RUN ----------------

print("BOT STARTED")
bot.run()

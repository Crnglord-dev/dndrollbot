import os
import re
import random
import telebot
from telebot import types

# Retrieve the Telegram bot token from environment variable
TOKEN = "**********************"
bot = telebot.TeleBot(TOKEN)

# Supported dice types
SUPPORTED_DICE = {'4', '6', '8', '12', '20'}

@bot.message_handler(commands=['rolld4', 'rolld6', 'rolld8', 'rolld12', 'rolld20'])
def handle_roll(message):
    # Extract the command (e.g., '/rolld20@MyBot')
    command = message.text.split()[0]
    # Extract dice sides using regex
    match = re.search(r'rolld(\d+)', command)
    if not match:
        return
    sides = match.group(1)
    if sides not in SUPPORTED_DICE:
        return

    # Roll the dice
    result = random.randint(1, int(sides))

    # Construct the path to the image
    script_dir = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(script_dir, 'images', f'd{sides}', f'{result}.jpg')

    # Prepare reply text
    user_handle = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    reply_text = f"{user_handle} rolled a d{sides}."

    # Send photo with caption (text+image in one message)
    if os.path.isfile(image_path):
        with open(image_path, 'rb') as img:
            bot.send_photo(
                message.chat.id,
                img,
                caption=reply_text,
                reply_to_message_id=message.message_id
            )
    else:
        # Fallback to sending text only if image is missing
        bot.reply_to(message, reply_text + "\n[Image not found for this roll]")

if __name__ == '__main__':
    print("Bot is polling...")
    bot.infinity_polling()

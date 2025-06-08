from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Command list to show as buttons
bot_commands = [
    ("start", "Start"),
    ("help", "Help"),
    ("weather", "Weather"),
    ("news", "News"),
    ("joke", "Joke"),
    ("quote", "Quote"),
    ("about", "About")
]

# /menu command handler
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []

    # Build rows of 2 buttons each
    for i in range(0, len(bot_commands), 2):
        row = [
            InlineKeyboardButton(f"/{bot_commands[i][0]}", callback_data=bot_commands[i][0])
        ]
        if i + 1 < len(bot_commands):
            row.append(InlineKeyboardButton(f"/{bot_commands[i + 1][0]}", callback_data=bot_commands[i + 1][0]))
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📋 Please choose a command:", reply_markup=reply_markup)

# Callback when button is clicked
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cmd = query.data

    # Optional: simulate running the command
    await query.edit_message_text(f"You selected `/{cmd}`", parse_mode="Markdown")

# Main bot setup
async def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(handle_button))

    await app.run_polling()

import asyncio
asyncio.run(main())

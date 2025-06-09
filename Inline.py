from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Start Aura", callback_data='start_aura')],
        [InlineKeyboardButton("Set Reminder", callback_data='set_reminder')],
        [InlineKeyboardButton("Convert File", callback_data='convert_file')],
        [InlineKeyboardButton("Manage Tasks", callback_data='manage_tasks')],
        [InlineKeyboardButton("Create Poll", callback_data='create_poll')],
        [InlineKeyboardButton("YouTube Downloader", callback_data='youtube_downloader')],
        [InlineKeyboardButton("Image/Gig Search", callback_data='image_gig_search')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an option:', reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    # Here you can handle what happens when a button is pressed
    if data == 'start_aura':
        query.edit_message_text(text="You chose: Start Aura")
    elif data == 'set_reminder':
        query.edit_message_text(text="You chose: Set Reminder")
    elif data == 'convert_file':
        query.edit_message_text(text="You chose: Convert File")
    elif data == 'manage_tasks':
        query.edit_message_text(text="You chose: Manage Tasks")
    elif data == 'create_poll':
        query.edit_message_text(text="You chose: Create Poll")
    elif data == 'youtube_downloader':
        query.edit_message_text(text="You chose: YouTube Downloader")
    elif data == 'image_gig_search':
        query.edit_message_text(text="You chose: Image/Gig Search")

def main():
    updater = Updater("YOUR_BOT_TOKEN")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

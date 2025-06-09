def send_reminder():
            time.sleep(delay)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Reminder: {task}")

        threading.Thread(target=send_reminder).start()

    except:
        update.message.reply_text("Invalid time format. Please enter like '15m' or '2h'.")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Reminder cancelled.")
    return ConversationHandler.END

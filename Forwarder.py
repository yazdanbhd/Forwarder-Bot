from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters


def start(update, context):
    if 'channels' not in context.user_data:
        context.bot.send_message(chat_id=update.message.chat_id, text="Hi there, please send me a list of usernames of channels that the bot is a admin of it separated by comma")
        return SELECT_CHANNEL
    else:
        buttons = []
        buttons.append([InlineKeyboardButton("Send to All Channels", callback_data="all")])
        for channel in context.user_data['channels']:
            buttons.append([InlineKeyboardButton(channel, callback_data=channel)])
        reply_markup = InlineKeyboardMarkup(buttons)
        context.bot.send_message(chat_id=update.message.chat_id, text="Please select a channel:", reply_markup=reply_markup)
        return MESSAGE


def select_channel(update, context):
    channels = update.message.text.split(",")
    channels = [x.strip() for x in channels]
    context.user_data['channels'] = channels
    buttons = []
    for channel in channels:
        buttons.append([InlineKeyboardButton(channel, callback_data=channel)])
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.message.chat_id, text="Please select a channel:", reply_markup=reply_markup)
    return MESSAGE


def message(update, context):
    query = update.callback_query
    if context.user_data.get("selected_channel") == "all":
        for channel in context.user_data['channels']:
            if update.message.photo:
                context.bot.send_photo(chat_id=channel, photo=update.message.photo[-1].file_id, caption=update.message.caption)
            elif update.message.document:
                context.bot.send_document(chat_id=channel, document=update.message.document.file_id, caption=update.message.caption)
            elif update.message.video:
                context.bot.send_video(chat_id=channel, video=update.message.video.file_id, caption=update.message.caption)
            else:
                context.bot.send_message(chat_id=channel, text=update.message.text)
    else:
        selected_channel = context.user_data["selected_channel"]
        if update.message.photo:
            context.bot.send_photo(chat_id=selected_channel, photo=update.message.photo[-1].file_id, caption=update.message.caption)
        elif update.message.document:
            context.bot.send_document(chat_id=selected_channel, document=update.message.document.file_id, caption=update.message.caption)
        elif update.message.video:
            context.bot.send_video(chat_id=selected_channel, video=update.message.video.file_id, caption=update.message.caption)
        else:
            context.bot.send_message(chat_id=selected_channel, text=update.message.text)
    return ConversationHandler.END


def button(update, context):
    query = update.callback_query
    selected_channel = query.data
    context.user_data["selected_channel"] = selected_channel
    context.bot.send_message(chat_id=query.message.chat_id, text="Selected channel: {} , please send a message to it.".format(selected_channel))
    return MESSAGE


def cancel(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Conversation cancelled.")
    return ConversationHandler.END


def help_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="""
Available commands:
- /start: Start the bot
- /add <channel_username>: Add a channel
- /remove <channel_username>: Remove a channel
- /help: Show this help message
""")


def error(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="An error has occurred.")

SELECT_CHANNEL, MESSAGE = range(2)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SELECT_CHANNEL: [MessageHandler(Filters.text, select_channel)],
        MESSAGE: [MessageHandler(Filters.text | Filters.document.mime_type("image/jpeg/mp4/mkv") | Filters.photo | Filters.video, message),
                  CallbackQueryHandler(button, pattern='^.*$')],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True,
    per_user=True,
    per_chat=True,
)


def main():
    updater = Updater(token="YOUR_BOT_TOKEN", use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("help", help_command))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
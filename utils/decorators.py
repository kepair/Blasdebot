from functools import wraps

import telegram
from telegram import ChatAction

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(bot, update, **kwargs):
            bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=action
            )
            return func(bot, update, **kwargs)

        return command_func

    return decorator

send_typing_action = send_action(ChatAction.TYPING)
send_recording_action = send_action(ChatAction.RECORD_AUDIO)
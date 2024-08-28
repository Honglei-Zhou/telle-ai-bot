from .bot_handler import handle_message, handle_close

handler = {
    'UPDATE_MSG': handle_message,
    'UPDATE_CHAT': handle_close
}
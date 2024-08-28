from chatbot.utils.detect_intent import detect_intent_texts
import json
from server.redis_instance import r


def handle_message(data):
    if data['tag'] == 'customer':
        if 'muted' in data and not data['muted']:
            to_room_id = data['groupId']
            dealer_id = data['dealerId']
            message = data['message']
            new_message = detect_intent_texts(to_room_id, message)

            r.publish('telle_ai_chat', json.dumps({'type': 'UPDATE_MESSAGE',
                                                   'dealerId': dealer_id,
                                                   'sid': to_room_id,
                                                   'message': new_message,
                                                   'tag': 'bot',
                                                   'unread': 1}))

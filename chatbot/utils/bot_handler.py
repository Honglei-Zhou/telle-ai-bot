from .detect_intent import detect_intent_texts
import json
from server.redis_instance import r


def handle_message(data):
    if 'user' in data and data['user'] == 'customer':
        if 'muted' in data and not data['muted']:
            # print(data)
            to_room_id = data['groupId']
            dealer_id = data['dealerId']
            message = data['message']
            new_message = detect_intent_texts(dealer_id, to_room_id, message)

            message_data = json.dumps({'type': 'UPDATE_MSG',
                                       'dealerId': dealer_id,
                                       'groupId': to_room_id,
                                       'user': 'bot',
                                       'muted': data['muted'],
                                       'unread': 1,
                                       'message': new_message})

            print('From bot: {}'.format(message_data))

            r.rpush('telle:queue:daemon', message_data)

            r.publish('telle_ai_chat', message_data)


def handle_close(data):
    if 'user' in data and data['user'] == 'customer':
        if 'muted' in data and not data['muted']:
            # print(data)
            to_room_id = data['groupId']
            dealer_id = data['dealerId']
            # message = data['message']
            message = {'data': {'text': 'CUSTOMERHASLEFT'}}
            detect_intent_texts(dealer_id, to_room_id, message)

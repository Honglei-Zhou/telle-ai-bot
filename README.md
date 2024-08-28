### Telle AI Bot

### Description 
This project is part of Telle AI Chatbot System. The bot is used to process user messages.

### Interfaces/APIs


```buildoutcfg

message type: dictionary
message: {'type': 'UPDATE_MSG', 
          'dealerId': dealerId,
          'groupId': groupId,
          'adminId': adminId, # required if user is admin
          'user': 'admin|customer|bot',
          'muted': True|False,
          'unread': 0,
          'message': message
         }
   
```
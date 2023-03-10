##### ASYNC 2



from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
        
    async def connect(self):
        user_id = self.scope["session"]["_auth_user_id"]
        self.group_name = "{}".format(user_id)
        # Join room group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None,bytes_data = None):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'recieve_group_message',
                'message': message
            }
        )

    async def recieve_group_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(
             text_data=json.dumps({
            'message': message
        }))









# #ASYNC
# import json

# from channels.generic.websocket import AsyncWebsocketConsumer


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": message}))









######### SINHRON
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

# import json


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         # ?????????? ????????????
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name

#         # ??????????????
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         # ??????????????????????????
#         self.accept()

#     def disconnect(self, close_code):
#         #
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # ???????????????? ???? ?????????????????? ?? ????????????????????
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # ???????????????? ?? ???????????? 
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 "type": "chat_message",
#                 "message": message
#             }
#         )

#     # ???????????????? ???????????? 
#     def chat_message(self, event):
#         message = event["message"]

#         # 
#         self.send(text_data=json.dumps({
#             "message": message
#         }))

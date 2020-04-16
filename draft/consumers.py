from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, SyncConsumer
import json



class DraftConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'draft_%s' % self.room_id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'draft_refresh',
                'message': message
            }
        )

    def draft_refresh(self, event):
        message = event['message']

        # Send message from room group
        self.send(text_data=json.dumps({
            'message': message
        }))

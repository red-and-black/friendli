import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from conversations.forms import MessageForm


class MessageConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.user_group_name = _get_user_group_name(self.user)

        # Join the user group.
        async_group_add = async_to_sync(self.channel_layer.group_add)
        async_group_add(self.user_group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        # Leave the user group.
        async_group_discard = async_to_sync(self.channel_layer.group_discard)
        async_group_discard(self.user_group_name, self.channel_name)

    def receive(self, text_data):
        user = self.user
        # Convert the string to a dictionary. It should have only these keys:
        # "content", "conversation".
        data = json.loads(text_data)

        # Validate the data.
        form = MessageForm(data, user=user)
        if form.is_valid():
            conversation = form.cleaned_data['conversation']
            recipient = conversation.other_party(user)
            user_blocked_by_recipient = user in recipient.profile.blocked.all()
            message = form.save(user_blocked_by_recipient)
        else:
            raise Exception(form.errors)

        # Build the wrapped payload to send to groups.
        wrapped_payload = {
            'type': 'conversation_message',
            'content': message.content,
            'conversation': conversation.pk,
            'sender': user.pk,
            'sender_username': self.user.username,
        }

        # Prepare to send the wrapped payload to groups.
        async_group_send = async_to_sync(self.channel_layer.group_send)

        # Send wrapped payload to sender user group.
        async_group_send(self.user_group_name, wrapped_payload)

        # Send wrapped payload to recipient user group.
        if not user_blocked_by_recipient:
            recipient_user_group_name = _get_user_group_name(recipient)
            async_group_send(recipient_user_group_name, wrapped_payload)

    # Receive message from user group.
    def conversation_message(self, event):
        payload = {
            'content': event['content'],
            'conversation': event['conversation'],
            'sender': event['sender'],
            'sender_username': event['sender_username'],
        }

        # Send message to WebSocket.
        self.send(text_data=json.dumps(payload))


def _get_user_group_name(user):
    return f'user_{user.pk}'

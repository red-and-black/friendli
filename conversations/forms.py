from django import forms
from django.db import transaction

from conversations.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(
                attrs={'autofocus': True, 'rows': 2}
            ),
        }

    def save(self, user, conversation, blocked_by_recipient):
        message = super(MessageForm, self).save(commit=False)
        message.conversation = conversation
        message.sender = user

        with transaction.atomic():
            message.save()
            conversation.update_latest_message(message)
            if not blocked_by_recipient:
                conversation.increment_unread_count(user)

        return message

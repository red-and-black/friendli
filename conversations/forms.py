from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction

from conversations.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content', 'conversation')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        # Ensure the user is in the conversation.
        conversation = self.cleaned_data.get("conversation")
        if not conversation.involves(self.user):
            raise ValidationError(
                f"User {self.user.username} is not in conversation "
                f"{conversation.pk}."
            )

    def save(self, blocked_by_recipient):
        message = super().save(commit=False)
        message.sender = self.user
        message.receiver = message.conversation.other_party(self.user)

        with transaction.atomic():
            message.save()
            message.conversation.update_latest_message(message)
            if not blocked_by_recipient:
                message.conversation.increment_unread_count(self.user)

        return message


class NewConversationForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(
                attrs={'autofocus': True, 'rows': 2}
            ),
        }

    def save(self, user, conversation, blocked_by_recipient):
        message = super(NewConversationForm, self).save(commit=False)
        message.conversation = conversation
        message.sender = user
        message.receiver = message.conversation.other_party(user)

        with transaction.atomic():
            message.save()
            conversation.update_latest_message(message)
            if not blocked_by_recipient:
                conversation.increment_unread_count(user)

        return message

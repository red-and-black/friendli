from hashlib import sha256

from django.conf import settings
from django.db import models
from django.db.models import Q

from conversations.utils import (
    conversation_time,
    message_time,
)


class ConversationManager(models.Manager):
    def between(self, user_1, user_2):
        """
        Accepts two users.

        Returns a conversation if one exists between the two users, or None if
        there is no conversation.

        Raises an exception if more than one conversation is returned.
        """
        try:
            return self.get_queryset().get(
                Q(approachee=user_1) & Q(initiator=user_2)
                | Q(approachee=user_2) & Q(initiator=user_1)
            )
        except Conversation.DoesNotExist:
            return None

    def involving(self, user):
        """
        Accepts a user.

        Returns a queryset of conversations to which the user is a party.
        """
        return self.get_queryset().filter(
            Q(approachee=user) | Q(initiator=user)
        )


class Conversation(models.Model):
    # Automatic timestamping fields.
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Relationship fields.
    approachee = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='conversations_as_approachee',
    )
    initiator = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='conversations_as_initiator',
    )
    latest_message = models.ForeignKey(
        'Message',
        on_delete=models.PROTECT,
        related_name='conversations',
        null=True,
    )

    # Ordinary fields.
    approachee_unread_count = models.PositiveSmallIntegerField(default=0)
    initiator_unread_count = models.PositiveSmallIntegerField(default=0)
    latest_message_time = models.DateTimeField(null=True)

    # Model managers.
    objects = models.Manager()
    c_objects = ConversationManager()

    class Meta:
        ordering = ['-latest_message']

    def __str__(self):
        return (
            'Conversation initiated by %s with %s.'
            % (self.initiator, self.approachee)
        )

    def increment_unread_count(self, user):
        """
        Increments the unread count for the appropriate user.

        Returns None.
        """
        if user == self.initiator:
            self.approachee_unread_count += 1
        else:
            self.initiator_unread_count += 1

        self.save()

    def involves(self, user):
        """
        Returns a boolean indicating whether the user is a party to the
        conversation.
        """
        return user in (self.initiator, self.approachee)

    def other_party(self, user):
        """
        Accepts a user who is presumed to be a party to the conversation.

        Returns the other party if the user is a party to the conversation.

        Raises an exception if the user is not a party to the conversation.
        """
        if user == self.initiator:
            return self.approachee
        elif user == self.approachee:
            return self.initiator
        else:
            raise Exception(
                'User "%s" is not a party to the conversation.' % user
            )

    def reset_unread_count(self, user):
        """
        Resets the unread count for the appropriate user.

        Returns None.
        """
        if user == self.initiator:
            self.initiator_unread_count = 0
        else:
            self.approachee_unread_count = 0

        self.save()

    @property
    def time(self):
        """
        Returns a human-readable string indicating the time since the latest
        message in the conversation.
        """
        return conversation_time(self.latest_message_time)

    @property
    def video_chat_url(self):
        """
        Returns the url of a video chat room just for the parties to the
        conversation if the approachee has responded, else returns None.
        """
        approachee_has_responded = self.messages.\
            filter(sender=self.approachee).\
            exists()

        if not approachee_has_responded:
            return None

        combined_usernames = "%s-and-%s" % (
            self.initiator.username.lower()[:15],
            self.approachee.username.lower()[:15],
        )
        token_input = "%s%s" % (combined_usernames, settings.SECRET_KEY)
        token = sha256(token_input.encode("utf-8")).hexdigest()[:10]

        return "https://meet.jit.si/%s-%s" % (combined_usernames, token)

    def update_latest_message(self, message):
        """
        Updates the latest message and latest message time.

        Returns None.
        """
        self.latest_message = message
        self.latest_message_time = message.created

        self.save()


class Message(models.Model):
    # Automatic timestamping field.
    created = models.DateTimeField(auto_now_add=True)

    # Relationship fields.
    conversation = models.ForeignKey(
        'conversations.Conversation',
        on_delete=models.PROTECT,
        related_name='messages',
    )
    receiver = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='received_messages',
    )
    sender = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='sent_messages',
    )

    # Ordinary fields.
    content = models.TextField(max_length=2000)  # TODO: Change length?
    is_read = models.BooleanField(default=False)

    class Meta:
        get_latest_by = ['created']
        ordering = ['created']

    @property
    def time(self):
        return message_time(self.created)

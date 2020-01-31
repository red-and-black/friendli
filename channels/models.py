from django.db import models

from conversations.utils import message_time


class Channel(models.Model):
    # Automatic timestamping fields.
    created = models.DateTimeField(auto_now_add=True)

    # Ordinary fields.
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']


class Post(models.Model):
    # Automatic timestamping fields.
    created = models.DateTimeField(auto_now_add=True)

    # Relationship fields.
    channel = models.ForeignKey(
        'channels.Channel',
        on_delete=models.PROTECT,
        related_name='posts',
    )
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
    )

    # Ordinary fields.
    content = models.CharField(max_length=2000)

    class Meta:
        get_latest_by = ['created']
        ordering = ['created']

    @property
    def time(self):
        return message_time(self.created)

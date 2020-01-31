from django import forms

from channels.models import (
    Channel,
    Post,
)


class ChannelForm(forms.ModelForm):
    """
    A form to add or edit a channel.
    """
    class Meta:
        model = Channel
        fields = ('description', 'name',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(
                attrs={'autofocus': True, 'rows': 2}
            ),
        }

    def save(self, user, channel):
        post = super(PostForm, self).save(commit=False)
        post.author = user
        post.channel = channel
        post.save()

        return post

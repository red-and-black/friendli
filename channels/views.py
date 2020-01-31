from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from channels.forms import PostForm
from channels.models import Channel


@login_required
def channel(request, name):
    """
    Show a page containing all the posts in a channel.
    """
    # Get the channel, or 404 if doesn't exist.
    channel = get_object_or_404(Channel, name=name)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save(request.user, channel)
            return redirect('channel', name)
    else:
        form = PostForm()

    return render(request, 'channel.html', {
        'channel': channel,
        'form': form,
    })


@login_required
def channels(request):
    """
    Show a page containing all the channels.
    """
    return render(request, 'channels.html', {
        'channels': Channel.objects.all(),
    })

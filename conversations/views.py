from copy import copy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q
from django.http import (
    Http404,
    JsonResponse,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from conferences.models import Conference
from profiles.models import (
    Blocked,
    Profile,
)
from conversations.forms import MessageForm
from conversations.models import Conversation


@login_required
def conversation(request, pk):
    """
    Show a page containing all the messages in this conversation.
    """
    user = request.user
    blocking_profiles = request.user.blocking_profile.all()
    blocked_users = Profile.objects.get(user=request.user).blocked.all()

    # Get the conversation, or 404 if doesn't exist.
    conversation = get_object_or_404(Conversation, pk=pk)

    # 404 if user isn't a party to the conversation.
    if not conversation.involves(user):
        raise Http404

    # Get the other party to the conversation.
    other_party = conversation.other_party(user)

    # Check if conversation is blocked by other party
    if other_party.profile in blocking_profiles:
        blocked_by_other = True
    else:
        blocked_by_other = False

    # Check if conversation is blocked by request user
    if other_party in blocked_users:
        blocked_by_user = True
    else:
        blocked_by_user = False

    # Get the messsages in the conversation.
    messages = conversation.messages.all()
    read_messages = messages.exclude(sender=other_party, is_read=False)
    unread_messages = messages.filter(sender=other_party, is_read=False)
    if blocked_by_user:
        block_time = Blocked.objects.\
            get(blocking_profile=user.profile, blocked_user=other_party).\
            timestamp
        unread_messages = unread_messages.exclude(created__gte=block_time)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(user, conversation, blocked_by_other)

            return redirect('conversation', pk)
    else:
        if unread_messages:
            with transaction.atomic():
                conversation.reset_unread_count(user)

                # The message.save() operation below modifies the read_messages
                # queryset, adding the saved messages to it. Therefore to be
                # able to use the current state of read_messages where it's
                # needed in the template, make a copy of it now.
                read_messages_copy = copy(read_messages)

                # Make every one of this user's unread messages in this
                # conversation as read.
                for message in unread_messages:
                    message.is_read = True
                    message.save()

                # Now restore the correct data to read_messages.
                read_messages = read_messages_copy

        form = MessageForm()

    return render(request, 'conversation.html', {
        'blocked_by_user': blocked_by_user,
        'conversation': conversation,
        'form': form,
        'other_party': other_party,
        'read_messages': read_messages,
        'unread_messages': unread_messages,
    })


@login_required
def conversations(request):
    """
    Show a page containing all the user's conversations.
    """
    user = request.user
    blocked_users = Profile.objects.get(user=request.user).blocked.all()
    conversation_list = Conversation.c_objects.involving(user)
    blocked_conversations = conversation_list.filter(
        Q(approachee__in=blocked_users) | Q(initiator__in=blocked_users)
    )
    unblocked_conversations = conversation_list.exclude(
        Q(approachee__in=blocked_users) | Q(initiator__in=blocked_users)
    )
    return render(request, 'conversations.html', {
        'conversations': unblocked_conversations,
        'blocked_conversations': blocked_conversations,
    })


@login_required
def start_conversation(request, pk):
    """
    Show a page which allows a user to start a conversation.

    Accepts the pk of the user to start the conversation with.
    """
    user = request.user
    other_party = get_object_or_404(User, pk=pk)

    # A user can't start a conversation with themselves.
    if user == other_party:
        raise Http404

    # A user can't start a conversation with someone who has blocked them.
    blocking_profiles = user.blocking_profile.all()
    blocked_by_other = (other_party in blocking_profiles)
    if blocked_by_other:
        raise Http404

    # If these two users already have a conversation, then redirect to that.
    existing_conversation = Conversation.c_objects.between(user, other_party)
    if existing_conversation:
        return redirect('conversation', existing_conversation.pk)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                conversation = Conversation.objects.create(
                    initiator=user,
                    approachee=other_party,
                )
                form.save(user, conversation, blocked_by_other)

            return redirect('conversation', conversation.pk)
    else:
        form = MessageForm()

    return render(request, 'start_conversation.html', {
        'form': form,
        'other_party': other_party,
    })


@login_required
def unread_messages(request):
    """
    Return a user's unread message counts as JSON.
    """
    user = request.user
    conversations = Conversation.c_objects.with_unread_messages(user)

    count_list = []
    for conversation in conversations:
        if conversation.initiator == user:
            count = conversation.initiator_unread_count
        else:
            count = conversation.approachee_unread_count
        count_list.append({'id': conversation.id, 'count': count})

    polling_interval = cache.get('polling_interval')
    if not polling_interval:
        polling_interval = Conference.objects.get().polling_interval
        cache.set('polling_interval', polling_interval, 60)

    response = {
        'messages': count_list,
        'wait': polling_interval,
    }

    return JsonResponse(response, safe=False)

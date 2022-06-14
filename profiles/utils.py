import re

from django.db.models import Q

from profiles.models import Profile


def get_search_results(user, search_data):
    """
    Accepts a user and a dictionary of cleaned data from the search form.

    Returns a queryset of search results.
    """
    blocking_users = user.blocking_profile.all()
    blocked_users = Profile.objects.get(user=user).blocked.all()
    blocked_profiles = [u.profile for u in blocked_users]

    languages = search_data['languages']
    looking_for = search_data['looking_for']
    prof_interests = search_data['prof_interests']
    personal_interests = search_data['personal_interests']
    detail = search_data['detail']
    ask_me = search_data['ask_me']
    teach_me = search_data['teach_me']

    search_expression = {}
    if languages not in [[], ['']]:  # TODO: Fix this.
        try:
            languages.remove('')
        except ValueError:
            pass
        search_expression['languages__in'] = languages
    if looking_for not in [[], ['']]:  # TODO: Fix this.
        try:
            looking_for.remove('')
        except ValueError:
            pass
        search_expression['looking_for__in'] = looking_for
    if prof_interests not in [[], ['']]:  # TODO: Fix this.
        try:
            prof_interests.remove('')
        except ValueError:
            pass
        search_expression['prof_interests__in'] = prof_interests
    if personal_interests not in [[], ['']]:  # TODO: Fix this.
        try:
            personal_interests.remove('')
        except ValueError:
            pass
        search_expression['personal_interests__in'] = \
            personal_interests

    q_list = []
    words_regex = re.compile(r'\w+')
    if detail:
        # TODO: Treat quoted strings as phrases.
        detail_words = words_regex.findall(detail)
        detail_q_object = Q()
        for word in detail_words:
            detail_q_object |= Q(detail__icontains=word)
        q_list.append(detail_q_object)
    if ask_me:
        # TODO: Treat quoted strings as phrases.
        ask_me_words = words_regex.findall(ask_me)
        ask_me_q_object = Q()
        for word in ask_me_words:
            ask_me_q_object |= Q(ask_me__icontains=word)
        q_list.append(ask_me_q_object)
    if teach_me:
        # TODO: Treat quoted strings as phrases.
        teach_me_words = words_regex.findall(teach_me)
        teach_me_q_object = Q()
        for word in teach_me_words:
            teach_me_q_object |= Q(teach_me__icontains=word)
        q_list.append(teach_me_q_object)

    search_results = Profile.objects.\
        filter(*q_list, **search_expression).\
        exclude(user__in=blocked_profiles).\
        exclude(user__in=blocking_users).\
        exclude(user=user).\
        exclude(user__pk=1).\
        distinct('pk')

    return search_results

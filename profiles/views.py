import re

from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import (
    Http404,
    JsonResponse,
)

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from friendli.decorators import public

from profiles.forms import (
    AddUserForm,
    EditUserForm,
    LoginForm,
    ProfileForm,
    ProfileSearchForm,
    UserSearchForm,
)

from profiles.models import (
    Blocked,
    Language,
    LookingFor,
    PersonalInterest,
    ProfessionalInterest,
    Profile,
    Starred,
)
from profiles.utils import get_search_results


@login_required
def blocked_list(request):
    blocks = Blocked.objects.filter(blocking_profile=request.user.profile)
    blocked_profiles = [block.blocked_user.profile for block in blocks]
    return render(request, 'blocked_list.html', {
        'blocked_profiles': blocked_profiles,
    })


@login_required
def profile_block(request, pk):
    profile = Profile.objects.get(user=request.user)
    blocked_user = User.objects.get(pk=pk)
    request_user_blocks = Profile.objects.get(user=request.user).blocked.all()
    request_user_stars = Profile.objects.get(user=request.user).starred.all()

    if blocked_user in request_user_blocks:
        profile.blocked.remove(blocked_user)
    else:
        with transaction.atomic():
            profile.blocked.add(blocked_user)
            if blocked_user in request_user_stars:
                profile.starred.remove(blocked_user)
    return redirect('blocked-list')


@login_required
def starred_list(request):
    stars = Starred.objects.filter(starring_profile=request.user.profile)
    starred_profiles = [star.starred_user.profile for star in stars]
    if starred_profiles:
        paginator = Paginator(starred_profiles, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None
    return render(request, 'starred_list.html', {
        'page_obj': page_obj,
    })


@login_required
def profile_star(request, pk):
    profile = Profile.objects.get(user=request.user)
    starred_user = User.objects.get(pk=pk)
    request_user_stars = Profile.objects.get(user=request.user).starred.all()
    if starred_user in request_user_stars:
        profile.starred.remove(starred_user)
        action = 'unstarred'
    else:
        profile.starred.add(starred_user)
        action = 'starred'

    response = {'user': starred_user.pk, 'action': action}
    return JsonResponse(response)


@login_required
def username_search(request):
    starred_users = Profile.objects.get(user=request.user).starred.all()
    blocking_users = request.user.blocking_profile.all()
    blocked_users = Profile.objects.get(user=request.user).blocked.all()
    blocked_profiles = [u.profile for u in blocked_users]
    if request.method == 'POST':
        form = UserSearchForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            search_results = Profile.objects.\
                filter(user__username__icontains=username).\
                exclude(user__in=blocked_profiles).\
                exclude(user__in=blocking_users).\
                exclude(user=request.user).\
                exclude(user__pk=1)

            # Save the search expression to the session for reuse.
            request.session['user_search_username'] = username
    else:
        username = request.session.get('user_search_username')
        if username is not None:
            # TODO: De-duplicate this query and one one above.
            search_results = Profile.objects.\
                filter(user__username__icontains=username).\
                exclude(user__in=blocked_profiles).\
                exclude(user__in=blocking_users).\
                exclude(user=request.user).\
                exclude(user__pk=1)
            initial = {"username": username}
        else:
            search_results = None
            initial = None

        form = UserSearchForm(initial=initial)
    if search_results is not None:
        count = search_results.count()
        paginator = Paginator(search_results, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        search_data = {'username': username}
    else:
        count = None
        page_obj = None
        search_data = None

    return render(request, 'username_search.html', {
        'count': count,
        'form': form,
        'page_obj': page_obj,
        'search_data': search_data,
        'starred_users': starred_users,
    })


@login_required
def search(request):
    user = request.user
    starred_users = Profile.objects.get(user=user).starred.all()

    if request.method == 'POST':
        profile_form = ProfileSearchForm(request.POST)

        if profile_form.is_valid():
            search_data = profile_form.cleaned_data
            search_results = get_search_results(user, search_data)
            request.session['search_data'] = search_data

    else:
        search_data = request.session.get('search_data')
        if search_data is not None:
            search_results = get_search_results(user, search_data)
        else:
            search_results = None

        profile_form = ProfileSearchForm(initial=search_data)

    if search_results is not None:
        count = search_results.count()
        paginator = Paginator(search_results, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        count = None
        page_obj = None
        search_data = None

    natural_keyed_search_data = {}
    if search_results is not None:
        # Replace foreign keys in search data with the strings they represent.
        natural_keyed_search_data['languages'] = list(
            Language.objects.
            filter(pk__in=search_data['languages']).
            values_list('language', flat=True)
        )
        natural_keyed_search_data['looking_for'] = list(
            LookingFor.objects.
            filter(pk__in=search_data['looking_for']).
            values_list('looking_for', flat=True)
        )
        natural_keyed_search_data['prof_interests'] = list(
            ProfessionalInterest.objects.
            filter(pk__in=search_data['prof_interests']).
            values_list('prof_interest', flat=True)
        )
        natural_keyed_search_data['personal_interests'] = list(
            PersonalInterest.objects.
            filter(pk__in=search_data['personal_interests']).
            values_list('personal_interest', flat=True)
        )
        words_regex = re.compile(r'\w+')
        natural_keyed_search_data['ask_me'] = \
            words_regex.findall(search_data['ask_me'])
        natural_keyed_search_data['teach_me'] = \
            words_regex.findall(search_data['teach_me'])
        natural_keyed_search_data['detail'] = \
            words_regex.findall(search_data['detail'])

    return render(request, 'search.html', {
        'count': count,
        'page_obj': page_obj,
        'profile_form': profile_form,
        'search_data': natural_keyed_search_data,
        'starred_users': starred_users,
    })


@login_required
def clear_search(request):
    request.session.pop('search_data', None)
    return JsonResponse({'result': True})


@login_required
def clear_username_search(request):
    request.session.pop('user_search_username', None)
    return JsonResponse({'result': True})


@public
def login(request):
    message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Assume the user provided a username.
            user_matching_username = User.objects.\
                filter(username__iexact=username_or_email).\
                first()
            if user_matching_username:
                # Get the username from the user so it has the correct casing.
                username = user_matching_username.username
                user = authenticate(username=username, password=password)
            else:
                user = None

            # If the user didn't provide a username, assume they provided an
            # email address.
            if not user:
                user_matching_email = User.objects.\
                    filter(email__iexact=username_or_email).\
                    first()
                if user_matching_email:
                    username = user_matching_email.username
                    user = authenticate(username=username, password=password)

            # If there is an authenticated user, log them in.
            if user:
                auth_login(request, user)
                return redirect('conversations')
            else:
                message = 'Those credentials are incorrect.'

    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        'message': message,
    })


@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')


@public
def signup(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            with transaction.atomic():
                user = User.objects.create_user(
                    username,
                    email,
                    password=password,
                )
                Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('conversations')
    else:
        form = AddUserForm()

    return render(request, 'signup.html', {
        'form': form,
    })


@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user_form = EditUserForm(
            request.POST,
            instance=user
        )
        profile_form = ProfileForm(
            request.POST,
            instance=Profile.objects.get(user=user)
        )
        if profile_form.is_valid() and user_form.is_valid():
            with transaction.atomic():
                profile_form.save()
                user_form.save()
            return redirect('profile-detail', user.username)
    else:
        profile_form = ProfileForm(instance=Profile.objects.get(user=user))
        user_form = EditUserForm(instance=user)
    return render(request, 'profile_edit.html', {
        'profile_form': profile_form,
        'user': user,
        'user_form': user_form,
    })


@login_required
def profile_detail(request, username):
    user_to_view = get_object_or_404(User, username__iexact=username)
    profile_to_view = Profile.objects.get(user=user_to_view)
    request_user_stars = Profile.objects.get(user=request.user).starred.all()
    request_user_blocked = Profile.objects.get(user=request.user).blocked.all()
    if request.user in Profile.objects.get(user=user_to_view).blocked.all():
        raise Http404()

    profile_is_empty = not any([
        profile_to_view.languages.all().exists(),
        profile_to_view.looking_for.all().exists(),
        profile_to_view.personal_interests.all().exists(),
        profile_to_view.prof_interests.all().exists(),
        profile_to_view.detail,
        profile_to_view.ask_me,
        profile_to_view.teach_me,
        profile_to_view.twitter,
        profile_to_view.mastodon,
        profile_to_view.github,
        profile_to_view.pronouns,
    ])

    return render(request, 'profile_detail.html', {
        'profile_is_empty': profile_is_empty,
        'request_user_blocked': request_user_blocked,
        'request_user_stars': request_user_stars,
        'user_to_view': user_to_view,
        'profile_to_view': profile_to_view,
    })

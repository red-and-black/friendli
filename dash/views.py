from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import (
    redirect,
    render
)

from django.contrib.auth.models import User
from behaviour.forms import UpdateBehaviourReportForm
from behaviour.models import BehaviourReport

from conferences.forms import ConferenceForm
from conferences.models import Conference

from conversations.models import Conversation

from goodchat.decorators import superuser_required

from profiles.forms import (
    LanguageForm,
    LookingForForm,
    ProfInterestForm,
    PersonalInterestForm,
)

from profiles.models import (
    Blocked,
    Language,
    LookingFor,
    Profile,
    ProfessionalInterest,
    PersonalInterest,
)


@superuser_required
def dash(request):
    profile_count = Profile.objects.all().count()
    convo_count = Conversation.objects.all().count()
    reports_count = BehaviourReport.objects.all().count()
    blocks_count = Blocked.objects.all().count()

    return render(request, 'dash.html', {
        'blocks_count': blocks_count,
        'convo_count': convo_count,
        'profile_count': profile_count,
        'reports_count': reports_count,
    })


@superuser_required
def blocking(request):
    blocks = Blocked.objects.all()
    blocked_users = User.objects.\
        filter(blocking_profile__isnull=False).\
        distinct()

    return render(request, 'blocking.html', {
        'blocked_users': blocked_users,
        'blocks': blocks,
    })


@superuser_required
def add_conference(request):
    conference = Conference.objects.last()
    if request.method == 'POST':
        form = ConferenceForm(request.POST)
        if form.is_valid():
            conference = form.save()
            cache.set('polling_interval', conference.polling_interval, 60)
            return redirect('conference')
    else:
        form = ConferenceForm()
    return render(request, 'add_conference.html', {
        'conference': conference,
        'form': form,
    })


@superuser_required
def conference(request):
    conference = Conference.objects.last()
    return render(request, 'conference.html', {
        'conference': conference,
    })


@superuser_required
def edit_conference(request):
    conference = Conference.objects.get()
    if request.method == 'POST':
        form = ConferenceForm(request.POST, instance=conference)
        if form.is_valid():
            conference = form.save()
            cache.set('polling_interval', conference.polling_interval, 60)
            return redirect('conference')
    else:
        form = ConferenceForm(instance=conference)
    return render(request, 'edit_conference.html', {
        'conference': conference,
        'form': form,
    })


@superuser_required
def edit_language(request, pk):
    language = Language.objects.get(pk=pk)
    if request.method == 'POST':
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            language = form.save()
            return redirect('languages')
    else:
        form = LanguageForm(instance=language)
    return render(request, 'edit_language.html', {
        'form': form,
        'language': language,
    })


@superuser_required
def languages(request):
    languages = Language.objects.all()
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('languages')
    else:
        form = LanguageForm()
    return render(request, 'languages.html', {
        'form': form,
        'languages': languages,
    })


@superuser_required
def edit_looking_for(request, pk):
    looking_for = LookingFor.objects.get(pk=pk)
    if request.method == 'POST':
        form = LookingForForm(request.POST, instance=looking_for)
        if form.is_valid():
            looking_for = form.save()
            return redirect('looking-for')
    else:
        form = LookingForForm(instance=looking_for)
    return render(request, 'edit_looking_for.html', {
        'form': form,
        'looking_for': looking_for,
    })


@superuser_required
def looking_for(request):
    looking_for = LookingFor.objects.all()
    if request.method == 'POST':
        form = LookingForForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('looking-for')
    else:
        form = LookingForForm()
    return render(request, 'looking_for.html', {
        'form': form,
        'looking_for': looking_for,
    })


@superuser_required
def edit_personal_interest(request, pk):
    personal_interest = PersonalInterest.objects.get(pk=pk)
    if request.method == 'POST':
        form = PersonalInterestForm(request.POST, instance=personal_interest)
        if form.is_valid():
            personal_interest = form.save()
            return redirect('personal-interests')
    else:
        form = PersonalInterestForm(instance=personal_interest)
    return render(request, 'edit_personal_interest.html', {
        'form': form,
        'personal_interest': personal_interest,
    })


@superuser_required
def personal_interests(request):
    personal_interests = PersonalInterest.objects.all()
    if request.method == 'POST':
        form = PersonalInterestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personal-interests')
    else:
        form = PersonalInterestForm()
    return render(request, 'personal_interests.html', {
        'form': form,
        'personal_interests': personal_interests,
    })


@superuser_required
def edit_prof_interest(request, pk):
    prof_interest = ProfessionalInterest.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProfInterestForm(request.POST, instance=prof_interest)
        if form.is_valid():
            prof_interest = form.save()
            return redirect('prof-interests')
    else:
        form = ProfInterestForm(instance=prof_interest)
    return render(request, 'edit_prof_interest.html', {
        'form': form,
        'prof_interest': prof_interest,
    })


@superuser_required
def prof_interests(request):
    prof_interests = ProfessionalInterest.objects.all()
    if request.method == 'POST':
        form = ProfInterestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prof-interests')
    else:
        form = ProfInterestForm()
    return render(request, 'prof_interests.html', {
        'form': form,
        'prof_interests': prof_interests,
    })


@superuser_required
def reports(request):
    reports = BehaviourReport.objects.all()
    return render(request, 'reports.html', {
        'reports': reports,
    })


@superuser_required
def update_report(request, pk):
    report = BehaviourReport.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateBehaviourReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save()
            return redirect('reports')
    else:
        form = UpdateBehaviourReportForm(instance=report)
    return render(request, 'update_report.html', {
        'form': form,
        'report': report,
    })


@superuser_required
def user_list(request):
    profiles = Profile.objects.all()
    paginator = Paginator(profiles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user_list.html', {
        'page_obj': page_obj,
        'profiles': profiles,
    })

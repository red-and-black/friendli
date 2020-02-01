from django.shortcuts import (
    redirect,
    render,
)
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from behaviour.forms import BehaviourReportForm
from behaviour.models import BehaviourReport

from conferences.models import Conference

from profiles.models import Profile


@login_required
def new_report(request, pk):
    reportee = User.objects.get(pk=pk)
    conference = Conference.objects.get()
    coc_link = conference.coc_link

    if request.method == 'POST':
        form = BehaviourReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reportee = reportee
            report.save()
            return redirect('report-received', pk)
    else:
        form = BehaviourReportForm()
    return render(request, 'report.html', {
        'coc_link': coc_link,
        'form': form,
        'reportee': reportee,
        'reporter': request.user,
    })


@login_required
def my_reports(request):
    reports = BehaviourReport.objects.filter(reporter=request.user)
    blocked_users = Profile.objects.get(user=request.user).blocked.all()

    return render(request, 'my_reports.html', {
        'blocked_users': blocked_users,
        'reports': reports,
    })


@login_required
def report_received(request, pk):
    reportee = User.objects.get(pk=pk)
    blocked_users = Profile.objects.get(user=request.user).blocked.all()

    return render(request, 'report_received.html', {
        'blocked_users': blocked_users,
        'reportee': reportee,
    })

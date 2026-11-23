
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm
from jobs.models import Job
from applications.models import Application, Notification
from interviews.models import Interview


def home(request):
    return render(request, 'accounts/home.html')


def register(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

    else:
        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


@login_required
def dashboard(request):

    context = {}

    # Recruiter Dashboard Analytics
    if request.user.role == 'recruiter':

        total_jobs = Job.objects.filter(
            recruiter=request.user
        ).count()

        total_applications = Application.objects.filter(
            job__recruiter=request.user
        ).count()

        total_interviews = Interview.objects.filter(
            application__job__recruiter=request.user
        ).count()

        shortlisted_candidates = Application.objects.filter(
            job__recruiter=request.user,
            status='shortlisted'
        ).count()

        context = {
            'total_jobs': total_jobs,
            'total_applications': total_applications,
            'total_interviews': total_interviews,
            'shortlisted_candidates': shortlisted_candidates,
        }

    # Candidate Dashboard Analytics
    elif request.user.role == 'candidate':

        total_applications = Application.objects.filter(
            candidate=request.user
        ).count()

        pending_applications = Application.objects.filter(
            candidate=request.user,
            status='pending'
        ).count()

        shortlisted_applications = Application.objects.filter(
            candidate=request.user,
            status='shortlisted'
        ).count()

        total_interviews = Interview.objects.filter(
            application__candidate=request.user
        ).count()

        unread_notifications = Notification.objects.filter(
            candidate=request.user,
            is_read=False
        ).count()

        context = {
            'candidate_total_applications': total_applications,
            'pending_applications': pending_applications,
            'shortlisted_applications': shortlisted_applications,
            'candidate_total_interviews': total_interviews,
            'unread_notifications': unread_notifications,
        }

    return render(
        request,
        'accounts/dashboard.html',
        context
    )

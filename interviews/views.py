
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from applications.models import Application
from .forms import InterviewForm
from .models import Interview


@login_required
def schedule_interview(request, application_id):

    if request.user.role != 'recruiter':
        return redirect('dashboard')

    application = get_object_or_404(
        Application,
        id=application_id,
        job__recruiter=request.user
    )

    if request.method == 'POST':
        form = InterviewForm(request.POST)

        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()

            return redirect('recruiter_applications')

    else:
        form = InterviewForm()

    return render(
        request,
        'interviews/schedule_interview.html',
        {
            'form': form,
            'application': application
        }
    )


@login_required
def my_interviews(request):

    if request.user.role != 'candidate':
        return redirect('dashboard')

    interviews = Interview.objects.filter(
        application__candidate=request.user
    ).select_related(
        'application',
        'application__job'
    ).order_by(
        'interview_date',
        'interview_time'
    )

    return render(
        request,
        'interviews/my_interviews.html',
        {'interviews': interviews}
    )


@login_required
def recruiter_interviews(request):

    if request.user.role != 'recruiter':
        return redirect('dashboard')

    interviews = Interview.objects.filter(
        application__job__recruiter=request.user
    ).select_related(
        'application',
        'application__candidate',
        'application__job'
    ).order_by(
        'interview_date',
        'interview_time'
    )

    return render(
        request,
        'interviews/recruiter_interviews.html',
        {'interviews': interviews}
    )
@login_required
def update_interview_status(request, interview_id):

    if request.user.role != 'recruiter':
        return redirect('dashboard')

    interview = get_object_or_404(
        Interview,
        id=interview_id,
        application__job__recruiter=request.user
    )

    if request.method == 'POST':

        status = request.POST.get('status')

        if status in ['scheduled', 'completed', 'cancelled']:
            interview.status = status
            interview.save()

    return redirect('recruiter_interviews')
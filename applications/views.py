
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Application, Notification
from .forms import ApplicationForm
from .resume_parser import extract_resume_text
from jobs.models import Job


@login_required
def apply_job(request, job_id):

    if request.user.role != 'candidate':
        return redirect('dashboard')

    job = get_object_or_404(Job, id=job_id)

    # Prevent duplicate applications
    if Application.objects.filter(
        candidate=request.user,
        job=job
    ).exists():
        return render(
            request,
            'applications/already_applied.html',
            {'job': job}
        )

    if request.method == 'POST':
        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(commit=False)
            application.candidate = request.user
            application.job = job

            # Extract text from uploaded PDF resume
            application.resume.seek(0)

            application.parsed_resume_text = extract_resume_text(
                application.resume
            )

            application.save()

            return redirect('job_list')

    else:
        form = ApplicationForm()

    return render(
        request,
        'applications/apply_job.html',
        {'form': form, 'job': job}
    )


@login_required
def my_applications(request):

    if request.user.role != 'candidate':
        return redirect('dashboard')

    applications = Application.objects.filter(
        candidate=request.user
    ).order_by('-applied_at')

    return render(
        request,
        'applications/my_applications.html',
        {'applications': applications}
    )


@login_required
def recruiter_applications(request):

    if request.user.role != 'recruiter':
        return redirect('dashboard')

    applications = Application.objects.filter(
        job__recruiter=request.user
    ).select_related(
        'candidate', 'job'
    ).order_by('-applied_at')

    return render(
        request,
        'applications/recruiter_applications.html',
        {'applications': applications}
    )


@login_required
def update_application_status(request, application_id):

    if request.user.role != 'recruiter':
        return redirect('dashboard')

    application = get_object_or_404(
        Application,
        id=application_id,
        job__recruiter=request.user
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        valid_statuses = [
            'pending',
            'reviewed',
            'shortlisted',
            'rejected',
            'selected'
        ]

        if new_status in valid_statuses:

            old_status = application.status

            if old_status != new_status:

                application.status = new_status
                application.save(update_fields=['status'])

                status_display = application.get_status_display()

                Notification.objects.create(
                    candidate=application.candidate,
                    application=application,
                    message=(
                        f"Your application for "
                        f"{application.job.title} "
                        f"has been updated to {status_display}."
                    )
                )

    return redirect('recruiter_applications')


@login_required
def my_notifications(request):

    if request.user.role != 'candidate':
        return redirect('dashboard')

    notifications = Notification.objects.filter(
        candidate=request.user
    ).order_by('-created_at')

    return render(
        request,
        'applications/my_notifications.html',
        {'notifications': notifications}
    )


@login_required
def mark_notification_read(request, notification_id):

    if request.user.role != 'candidate':
        return redirect('dashboard')

    if request.method == 'POST':

        notification = get_object_or_404(
            Notification,
            id=notification_id,
            candidate=request.user
        )

        notification.is_read = True
        notification.save(update_fields=['is_read'])

    return redirect('my_notifications')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models

from .models import Job
from .forms import JobForm

from applications.models import Application
from applications.resume_parser import (
    extract_skills,
    calculate_skill_match,
    get_skill_details
)


@login_required
def post_job(request):

    if request.user.role != 'recruiter':
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()

            return redirect('my_jobs')

    else:
        form = JobForm()

    return render(
        request,
        'jobs/post_job.html',
        {'form': form}
    )


@login_required
def my_jobs(request):

    if request.user.role != 'recruiter':
        return redirect('dashboard')

    jobs = Job.objects.filter(
        recruiter=request.user
    ).order_by('-created_at')

    return render(
        request,
        'jobs/my_jobs.html',
        {'jobs': jobs}
    )


@login_required
def edit_job(request, job_id):

    if request.user.role != 'recruiter':
        return redirect('dashboard')

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect('my_jobs')

    else:
        form = JobForm(instance=job)

    return render(
        request,
        'jobs/edit_job.html',
        {'form': form, 'job': job}
    )


@login_required
def delete_job(request, job_id):

    if request.user.role != 'recruiter':
        return redirect('dashboard')

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )

    if request.method == 'POST':
        job.delete()
        return redirect('my_jobs')

    return render(
        request,
        'jobs/delete_job.html',
        {'job': job}
    )


@login_required
def job_list(request):

    jobs = Job.objects.all().order_by('-created_at')

    search_query = request.GET.get('search', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')

    # Search by job title or company
    if search_query:
        jobs = jobs.filter(
            models.Q(title__icontains=search_query) |
            models.Q(company__icontains=search_query)
        )

    # Filter by location
    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    # Filter by job type
    if job_type:
        jobs = jobs.filter(
            job_type__iexact=job_type
        )

    candidate_skills = []
    has_resume = False

    # Calculate candidate skill matches
    if request.user.role == 'candidate':

        latest_application = Application.objects.filter(
            candidate=request.user
        ).order_by('-applied_at').first()

        if latest_application and latest_application.parsed_resume_text:

            candidate_skills = extract_skills(
                latest_application.parsed_resume_text
            )

            has_resume = True

            for job in jobs:

                # Calculate skill match percentage
                job.match_percentage = calculate_skill_match(
                    candidate_skills,
                    job.required_skills
                )

                # Identify matched and missing skills
                matched, missing = get_skill_details(
                    candidate_skills,
                    job.required_skills
                )

                job.matched_skills = matched
                job.missing_skills = missing

    context = {
        'jobs': jobs,
        'search_query': search_query,
        'location': location,
        'selected_job_type': job_type,
        'candidate_skills': candidate_skills,
        'has_resume': has_resume,
    }

    return render(
        request,
        'jobs/job_list.html',
        context
    )

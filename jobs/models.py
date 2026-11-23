from django.db import models
from django.conf import settings


class Job(models.Model):

    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    title = models.CharField(max_length=200)

    company = models.CharField(max_length=200)

    location = models.CharField(max_length=150)

    salary = models.CharField(max_length=100, blank=True)

    job_type = models.CharField(max_length=50)

    description = models.TextField()

    required_skills = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
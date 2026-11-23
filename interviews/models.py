from django.db import models
from applications.models import Application


class Interview(models.Model):

    MODE_CHOICES = [
        ('online', 'Online'),
        ('in_person', 'In-Person'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='interviews'
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    mode = models.CharField(
        max_length=20,
        choices=MODE_CHOICES
    )

    meeting_link = models.URLField(blank=True)

    location = models.CharField(
        max_length=250,
        blank=True
    )

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview - {self.application.candidate.username}"
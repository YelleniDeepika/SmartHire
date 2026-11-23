
from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),

    path(
        'my-applications/',
        views.my_applications,
        name='my_applications'
    ),

    path(
        'my-notifications/',
        views.my_notifications,
        name='my_notifications'
    ),

    path(
        'recruiter-applications/',
        views.recruiter_applications,
        name='recruiter_applications'
    ),

    path(
        'update-status/<int:application_id>/',
        views.update_application_status,
        name='update_application_status'
    ),
    path(
    'mark-read/<int:notification_id>/',
    views.mark_notification_read,
    name='mark_notification_read'
),
]

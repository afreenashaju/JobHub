from django.urls import path
from . import views

urlpatterns = [
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),

    path(
        "edit/<int:job_id>/",
        views.edit_job,
        name="edit_job",
    ),
    path(
    "delete/<int:job_id>/",
    views.delete_job,
    name="delete_job",
),
]
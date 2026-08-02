from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.db.models import Q
import pandas as pd
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import (
    UploadCSVForm,
    PasteExcelForm,
    ApplicationForm,
    JobForm,
)
from .models import Job, Application
from django.contrib.auth.models import User


@login_required
def dashboard(request):

    if request.user.is_superuser:

        # Latest 5 applications
        recent_applications = Application.objects.select_related(
            "job"
        ).order_by("-applied_date")[:5]

        context = {

            "total_jobs": Job.objects.count(),

            "total_applications": Application.objects.count(),

            "total_users": User.objects.filter(
                is_superuser=False
            ).count(),

            "total_companies":
                Job.objects.values("company").distinct().count(),

            "active_jobs":
                Job.objects.count(),

            "recent_applications": recent_applications,

        }

        return render(
            request,
            "admin_dashboard.html",
            context,
        )

    return render(
        request,
        "candidate_dashboard.html",
    )

from django.db.models import Q
from django.db.models import Q

def job_list(request):

    jobs = Job.objects.all()

    # Search
    query = request.GET.get("q")

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query)
        )

    # Job Type Filter
    job_type = request.GET.get("job_type")

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    # Location Filter
    location = request.GET.get("location")

    if location:
        jobs = jobs.filter(location=location)

    # Sorting
    sort = request.GET.get("sort")

    if sort == "latest":
        jobs = jobs.order_by("-posted_date")

    elif sort == "oldest":
        jobs = jobs.order_by("posted_date")

    elif sort == "company":
        jobs = jobs.order_by("company")

    elif sort == "title":
        jobs = jobs.order_by("title")
    # Pagination
    paginator = Paginator(jobs, 6)

    page_number = request.GET.get("page")

    jobs = paginator.get_page(page_number)

    context = {

        "jobs": jobs,

        "query": query,

        "selected_job_type": job_type,

        "selected_location": location,

        "selected_sort": sort,

        "job_types": Job.objects.values_list(
            "job_type",
            flat=True
        ).distinct(),

        "locations": Job.objects.values_list(
            "location",
            flat=True
        ).distinct(),

        "total_jobs": paginator.count,

    }

    return render(request, "job_list.html", context)
#def upload_csv(request):
 #   return render(request, 'upload_csv.html')
def job_detail(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    return render(
        request,
        "job_detail.html",
        {"job": job}
    )
def upload_csv(request):
    if request.method == "POST":

        form = UploadCSVForm(request.POST, request.FILES)

        if form.is_valid():

            csv_file = request.FILES["csv_file"]

            try:

                df = pd.read_csv(csv_file)

                for _, row in df.iterrows():

                    #Job.objects.create(

#                        title=row["title"],

 #                       company=row["company"],

  #                      location=row["location"],

   #                     salary=row["salary"],

    #                    experience=row["experience"],

     #                   job_type=row["job_type"],

      #                  description=row["description"],
#
 #                       posted_date=row["posted_date"]

                    #)
                    Job.objects.get_or_create(
    title=row["title"],
    company=row["company"],
    defaults={
        "location": row["location"],
        "salary": row["salary"],
        "experience": row["experience"],
        "job_type": row["job_type"],
        "description": row["description"],
        "posted_date": row["posted_date"],
    }
)

                messages.success(request, "CSV uploaded successfully!")

                return redirect("/jobs/")

            except Exception as e:

                messages.error(request, str(e))

    else:

        form = UploadCSVForm()

    return render(request, "upload_csv.html", {"form": form})

def apply_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()

            messages.success(request, "Application submitted successfully!")
            return redirect("job_detail", job_id=job.id)

    else:
        form = ApplicationForm()

    return render(request, "apply_job.html", {
        "job": job,
        "form": form
    })


from datetime import datetime

def paste_excel(request):

    form = PasteExcelForm()

    if request.method == "POST":

        form = PasteExcelForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data["excel_data"]

            rows = data.strip().split("\n")

            count = 0

            for row in rows:

                cols = row.strip().split("\t")

                if len(cols) < 8:
                    continue

                try:
                    posted_date = datetime.strptime(
                        cols[7].strip(),
                        "%Y-%m-%d"
                    ).date()

                    Job.objects.create(
                        title=cols[0].strip(),
                        company=cols[1].strip(),
                        location=cols[2].strip(),
                        salary=cols[3].strip(),
                        experience=cols[4].strip(),
                        job_type=cols[5].strip(),
                        description=cols[6].strip(),
                        posted_date=posted_date
                    )

                    count += 1

                except Exception as e:
                    messages.error(request, f"Error: {e}")

            messages.success(
                request,
                f"{count} jobs imported successfully!"
            )

    return render(request, "paste_excel.html", {"form": form})
@login_required
def my_applications(request):

    applications = Application.objects.filter(
        email=request.user.email
    ).order_by("-applied_date")

    return render(
        request,
        "my_applications.html",
        {
            "applications": applications
        }
    )
@user_passes_test(lambda u: u.is_superuser)
def edit_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":

        form = JobForm(request.POST, instance=job)

        if form.is_valid():

            form.save()

            messages.success(request, "Job updated successfully!")

            return redirect("job_list")

    else:

        form = JobForm(instance=job)

    return render(
        request,
        "edit_job.html",
        {
            "form": form,
            "job": job,
        },
    )
@user_passes_test(lambda u: u.is_superuser)
def delete_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":

        job.delete()

        messages.success(
            request,
            "Job deleted successfully!"
        )

        return redirect("job_list")

    return render(
        request,
        "delete_job.html",
        {
            "job": job,
        },
    )
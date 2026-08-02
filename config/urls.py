# """
# URL configuration for config project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/6.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.contrib import admin
from django.urls import path
from django.urls import include
from jobs import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path("", include("jobs.urls")),
    path("users/", include("users.urls")),

    path('', views.dashboard, name='dashboard'),

    path('jobs/', views.job_list, name='job_list'),

    path('upload/', views.upload_csv, name='upload_csv'),

    path('paste/', views.paste_excel, name='paste_excel'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path(
    "my-applications/",
    views.my_applications,
    name="my_applications"
),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

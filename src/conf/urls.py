"""coopolis_backoffice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
]

urlpatterns += [
    path('', include('apps.coopolis.urls')),
    path('', include('apps.cc_users.urls')),
    path('', include('apps.cc_courses.urls')),
    path('', include('apps.projects.urls')),
]

# Add views for testing 404 and 500 templates
urlpatterns += [
    path('test404/', TemplateView.as_view(template_name='404.html')),
    path('test500/', TemplateView.as_view(template_name='500.html')),
]

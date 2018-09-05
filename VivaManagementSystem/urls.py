"""VivaManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^login/$', views.login),
    url(r'^index/$', views.index),
    url(r'^logout/$', views.logout),
    url(r'^config/$', views.config),
    url(r'^guide-allot/$', views.guide_allot),
    url(r'^guide-select/$', views.guide_select),
    url(r'^view-student', views.student_list),
    url(r'^about', views.about),
    url(r'^ajax/(?P<ajax_call>[a-zA-Z_]+)/$', views.ajax)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

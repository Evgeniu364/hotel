"""Hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from os import name


from django.conf.urls import url
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from .views import *


urlpatterns = [
    path('', index, name='mainapp_page'),
    path('bar/', bar_page, name='bar_page'),
    path('bar/recomendation', bar_page_recomendation, name='bar_page_recomendation'),
    path('bar/<str:type_alcohol>', filter_bar_page, name='filter_bar_page'),
    path('bar/<int:number>/', post_bar_page, name='post_bar_page'),
    path('booking/<str:type_room>/<int:count_person>', BookingCreate.as_view(), name='booking_create'),
    path('contact/', contact_page, name='contact_page'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
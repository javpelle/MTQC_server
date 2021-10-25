from django.conf.urls import url
from MTQCApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^login/$',views.login),
    url(r'^register/$',views.register),
]
from django.conf.urls import url
from MTQCApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^guestLogin/$', views.guest_login),
    url(r'^register/$', views.register),
    url(r'^changePassword/$', views.change_password),
    url(r'^verifyAccount/([0-9a-f]+)$', views.verify_account),
    url(r'^newProject/$', views.new_project),

]

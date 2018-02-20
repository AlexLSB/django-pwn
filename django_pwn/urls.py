# -*- coding: utf-8 -*-
from django.conf.urls import url

import views


urlpatterns = [
    # This URL is used to recieve notifications from PWN.
    # You have to inform PWN staff about the url you're
    # intending to use.
    url(r'^notif/$', views.NotifyView.as_view(), name='cart'),
]

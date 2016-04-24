from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.render_query_form),
    url(r'^blob$', views.retrieve_semantic_blob),
    url(r'^feedback$', views.feedback)
]

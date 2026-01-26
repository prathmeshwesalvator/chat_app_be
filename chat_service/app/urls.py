from django.contrib import admin
from django.urls import path
from app.views import ChatAPIView


from app import views


urlpatterns = [
    path("", views.root),
    path('get-contacts/' , ChatAPIView.as_view() , name = 'get-contacts'),
    path('create-contact/' , ChatAPIView.as_view() , name = 'create-contcat')
]

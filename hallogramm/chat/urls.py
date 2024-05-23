from django.urls import path, include
from . import views

app_name = 'chat'

urlpatterns = [
    path('<uuid:chat_uuid>/', views.show, name='show')
]

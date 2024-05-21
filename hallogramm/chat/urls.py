from django.urls import path, include
from . import views


urlpatterns = [
    path('<uuid:chat_uuid>/', views.show_chat, name='chat')
]

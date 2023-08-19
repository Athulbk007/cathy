from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.voice_assistant, name='voice_assistant'),
]

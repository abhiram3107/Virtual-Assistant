from django.urls import path
from .views import NavigationView
from . import views
urlpatterns = [
    path('chat/', NavigationView.as_view(), name='get_navigation'),
    path('hello/',views.Hello, name='hello')
]

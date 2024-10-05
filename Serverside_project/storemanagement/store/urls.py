from django.urls import path

from store import views

urlpatterns = [
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
]

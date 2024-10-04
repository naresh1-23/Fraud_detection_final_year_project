from django.urls import path
from app.views import user_views

urlpatterns = [
    path('login/', user_views.user_login, name='login')
]

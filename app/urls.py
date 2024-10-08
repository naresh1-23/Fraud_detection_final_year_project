from django.urls import path
from app.views import user_views
from app.views import product_views
from app.views import seller_views
from app.views import prakash_views

urlpatterns = [
    path('login/', user_views.user_login, name='login'),
    path('register/', user_views.register, name='register'),
    path('home/', product_views.home, name='home'),
    path('add_product/', seller_views.add_product, name='add product'),
    path('bid/', product_views.bid, name='bid'),
    path('data_listing/', prakash_views.data_listing, name='data listing'),
    path('win/', prakash_views.win, name='won')
]

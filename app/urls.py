from django.urls import path
from app.views import user_views
from app.views import product_views
from app.views import seller_views
from app.views import dataset_views
from app.views import prakash_views

urlpatterns = [
    path('login/', user_views.user_login, name='login'),
    path('register/', user_views.register, name='register'),
    path('', product_views.home, name='home'),
    path('add_product/', seller_views.add_product, name='add product'),
    path('bid/<int:pk>/', product_views.bid, name='bid'),
    path('logout/', user_views.user_logout, name='logout'),
    path('data_listing/', dataset_views.data_listing, name='data listing'),
    path('profile/', user_views.profile, name='profile'),
    path('your_product/', seller_views.your_product, name='your product'),
    path('bidder_bids/', product_views.bidder_bids, name='bidders bid'),
    path('bids_won/', product_views.bids_won, name='bids won')
]

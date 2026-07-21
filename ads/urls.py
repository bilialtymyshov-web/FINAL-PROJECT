from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('my-ads/', views.MyAdsListView.as_view(), name='my_ads'),
]
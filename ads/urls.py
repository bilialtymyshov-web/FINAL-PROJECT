from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/create/', views.AdCreateView.as_view(), name='ad_create'),
    path('ad/<int:pk>/edit/', views.AdUpdateView.as_view(), name='ad_update'),
    path('ad/<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad_delete'),
    path('my-ads/', views.MyAdsListView.as_view(), name='my_ads'),
]
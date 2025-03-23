from django.urls import path
from . import views

app_name = 'ad'
urlpatterns = [
    path('list', views.AdsListView.as_view(),name='list'),
    path('create', views.AdCreateView.as_view(),name='create'),
    path('detail/<int:pk>', views.AdDetailView.as_view(),name='detail'),
    path('edit/<int:pk>', views.AdEditView.as_view(),name='edit'),
    path('delete/<int:pk>', views.AdDeletetView.as_view(),name='delete'),
    path('search/', views.AdSearchView.as_view(),name='search'),
]
from _ast import pattern

from django.urls import path, include
from Blog import views

urlpatterns = [
    path('', views.StartingPageView.as_view(), name='starting-page'),
    path('posts/', views.AllPostsView.as_view(), name='posts-page'),
    path('posts/<slug:slug>', views.DetailPageView.as_view(), name='post-details-page'),
    path('read-later', views.ReadLaterView.as_view(), name='read-later'),
]

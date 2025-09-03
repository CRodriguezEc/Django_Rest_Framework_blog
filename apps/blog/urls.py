from django.urls import path

from .views import PostListView, PostDetailView, PostHeadingView

urlpatterns = [
    path('post/', PostListView.as_view(), name='post-list'),
    path('post/<slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/headings', PostHeadingView.as_view(), name='post-headings')
]
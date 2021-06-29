from django.urls import path, include
from .views import PostList, PostCreate, PostDetail, PostUpdate, PostDelete, LikeView

urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('post-create/', PostCreate.as_view(), name='post-create'),
    path('<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('<int:pk>/post-edit/', PostUpdate.as_view(), name='post-update'),
    path('<int:pk>/post-delete/', PostDelete.as_view(), name='post-delete'),
    path('like/', LikeView.as_view(), name='like-button'),
]

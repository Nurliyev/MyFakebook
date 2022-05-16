from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, RegisterView, activate

urlpatterns = [
    path('', include('posts.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]

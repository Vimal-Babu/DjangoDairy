from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Home,BlogPostCreateView,BlogPostDetailView,SignupView,LikePostView,CommentCreateView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('post/new/', BlogPostCreateView.as_view(), name='post-create'),  
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post-detail'), 
    path('post/<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='post-comment'),
    path('signup/', SignupView.as_view(), name='signup'),
]

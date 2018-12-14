from django.urls import path, include

from blog import views
from django.contrib.auth import views as auth_views

app_name='blog'
urlpatterns = [
    #path('login/', auth_views.LoginView as view())
    path('',views.index, name='index'),
    path('<int:pk>/',views.BlogView.as_view(), name='blog'),
    path('posts/<int:post_pk>/comment_add',views.CommentAdd.as_view(), name='comment_add'),
    path('blog_add/',views.BlogAdd.as_view(), name='blog_add'),
    path('<int:blog_pk>/post_add/',views.PostAdd.as_view(), name='post_add'),
    path('posts/<int:pk>/',views.PostView.as_view(), name='post'),  
    path('posts/<int:pk>/post_edit',views.PostEdit.as_view(), name='post_edit'),  
    path('my_blogs/',views.my_blogs, name='my_blogs'),  
    # path('registration/',views.UserAdd.as_view(), name='registration'),  
    path('registration/',views.user_add, name='registration'),  
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='blog/registration/login.html'), name='login'),  
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(template_name='blog/registration/logged_out.html'), name='logout'),  
    #path('accounts/', include('django.contrib.auth.urls')),
]

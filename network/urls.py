
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.profile, name="profile"),
    path("following", views.follow_user, name="follow_user"),
    path("bio", views.bio, name="bio"),
    
    # API routes:
    path("delete/", views.delete_post, name="delete"),
    path("edit/", views.edit_post, name="edit"),
    path("like/", views.like, name="like")
]

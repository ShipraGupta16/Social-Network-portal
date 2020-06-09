
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("add-post/", views.add_post, name="add-post"),
    path("edit-post/<int:post_id>", views.edit_post, name="edit-post"),
    path("following/", views.following, name="following"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("likeunlike/<int:post_id>", views.likeunlike, name="likeunlike"),
]

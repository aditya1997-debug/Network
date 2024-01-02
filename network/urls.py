
from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<slug:name>", views.profile, name="profile"),
    path("follow/<slug:person>", views.follow, name="follow"),
    path("edit/<int:id>", views.edit, name='edit'),
    path("following", views.following, name='following'),
    path("like/<int:id>", views.like, name='like'),
    path("profile/like/<int:id>", views.like, name='like'),
    path("delete/<int:id>", views.delete_post, name='edit'),
    path("profile/delete/<int:id>", views.delete_post, name='edit'),

]

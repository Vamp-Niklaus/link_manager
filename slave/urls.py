from django.contrib import admin
from django.urls import path
from slave import views

urlpatterns = [
    path("", views.index,name='home'),
    path("signup", views.signup,name='signup'),
    path("signin", views.signin,name='signin'),
    path("save", views.save,name='save'),
    path("signout", views.signout,name='signout'),
    path("fsave", views.fsave,name='fsave'),
    path("moco/<str:q>", views.moco,name='moco'),
    path("dmoco/<str:q>", views.dmoco,name='dmoco'),
    path("delete/<str:q>", views.delete,name='delete'),
    path("<str:path>", views.dir,name='dir'),
    # path("edit/<str:q>", views.edit,name='edit'),
]

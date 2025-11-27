from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('create-application/', views.create_application_view, name='create_application'),
    path('my-applications/', views.my_applications_view, name='my_applications'),
    path('delete-application/<int:application_id>/', views.delete_application_view, name='delete_application'),
]
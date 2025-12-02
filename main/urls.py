from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # главная страница
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('applications/create/', views.create_application_view, name='create_application'),
    path('applications/my/', views.my_applications_view, name='my_applications'),
    path('applications/delete/<int:application_id>/', views.delete_application_view, name='delete_application'),
    path('superadmin/', views.superadmin, name='superadmin'),
    path('superadmin/category/add/', views.add_category, name='add_category'),
    path('superadmin/category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('superadmin/application/change-status/<int:app_id>/<str:new_status>/', views.change_application_status,
         name='change_status'),
]
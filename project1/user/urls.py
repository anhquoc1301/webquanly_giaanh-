
from django.urls import path
from .views import dangnhap, view_users, add_user, edit_user, delete_user, view_camera, management_car, export_report, logout, edit_profile, demo

app_name='user'
urlpatterns = [
    path('', dangnhap.as_view(), name='login'),
    path('view_users/', view_users, name='view_users'),
    path('add_user/', add_user, name='add_user'),
    path('edit_user/<str:pk>/', edit_user, name='edit_user'),
    path('delete_user/<str:pk>/', delete_user, name='delete_user'),
    path('view_camera/', view_camera, name='view_camera'),
    path('management_car/', management_car, name='management_car'),
    path('export_report/', export_report, name='export_report'),
    path('logout/', logout, name='logout'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('demo/', demo, name='demo')


]
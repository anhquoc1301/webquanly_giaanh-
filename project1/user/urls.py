
from django.urls import path
from .views import LoginClass, view_camera, view_users, add_user, edit_user, delete_user, management_car, export_report, logout, edit_profile
from .views import import_excel_car, export_excel_cal, dowload_local_excel_car, add_managementcar, edit_managementcar, delete_managementcar, export_report_excel

app_name='user'
urlpatterns = [
    path('', LoginClass.as_view(), name='login'),
    path('view_users/', view_users, name='view_users'),
    path('add_user/', add_user, name='add_user'),
    path('edit_user/<str:pk>/', edit_user, name='edit_user'),
    path('delete_user/<str:pk>/', delete_user, name='delete_user'),
    path('view_camera/', view_camera, name='view_camera'),
    path('management_car/', management_car, name='management_car'),
    path('export_report/', export_report, name='export_report'),
    path('logout/', logout, name='logout'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('import_excel_car/', import_excel_car, name='import_excel_car'),
    path('export_excel_car/', export_excel_cal, name='export_excel_car'),
    path('dowload_local_excel_car/', dowload_local_excel_car, name='dowload_local_excel_car'),
    path('add_managementcar/', add_managementcar, name='add_managementcar'),
    path('edit_managementcar/<str:pk>/', edit_managementcar, name='edit_managementcar'),
    path('delete_managementcar/<str:pk>/', delete_managementcar, name='delete_managementcar'),
    path('export_report_excel/', export_report_excel, name='export_report_excel'),

]
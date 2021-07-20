from django.contrib import admin
from .models import User, Carmanagement, FileExcel_Carmanagement, CarNumber
from import_export.admin import ImportExportModelAdmin
# Register your models here.

admin.site.register(User)
admin.site.register(CarNumber)
@admin.register(Carmanagement)
class carmanagement(ImportExportModelAdmin):
    list_display = ( 'car_number', 'mass', 'driver', 'company')


@admin.register(FileExcel_Carmanagement)
class fileexcel_carmanagement(ImportExportModelAdmin):
    list_display = ( 'car_number', 'mass', 'driver', 'company')



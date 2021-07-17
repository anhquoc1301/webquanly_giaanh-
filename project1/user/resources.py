from import_export import resources
from .models import Carmanagement, FileExcel_Carmanagement

class Carmanagement_resources(resources.ModelResource):
    class Meta:
        model=Carmanagement


class FileExcel_Carmanagement_resources(resources.ModelResource):
    class Meta:
        model=FileExcel_Carmanagement
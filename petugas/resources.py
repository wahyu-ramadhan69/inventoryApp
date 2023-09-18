from inven.models import pegawai
from import_export import resources
from .models import *


class pegawaisumber(resources.ModelResource):
    class Meta:
        model = pegawai

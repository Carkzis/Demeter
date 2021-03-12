from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import Nation, Meal
from .resources import NationResource

admin.site.register(Meal)

class NationAdmin(ImportExportModelAdmin):
    resource_class = NationResource
    list_display = ('country', 'continent', 'national_dish',)

admin.site.register(Nation, NationAdmin)
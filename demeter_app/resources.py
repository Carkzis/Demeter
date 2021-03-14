from import_export import resources
from .models import Nation

class NationResource(resources.ModelResource):

    class Meta:
        model = Nation
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('country', 'continent', 'national_dish',)
        fields = ('country', 'continent', 'national_dish',)
from import_export import resources
from .models import Nation

class NationResource(resources.ModelResource):

    class Meta:
        model = Nation
        skip_unchanged = False
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('country', 'continent', 'national_dish',)
        fields = ('id', 'country', 'continent', 'national_dish',)
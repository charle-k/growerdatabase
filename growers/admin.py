from django.contrib import admin

from .models import Grower


class GrowerAdmin(admin.ModelAdmin):
    list_display = ('Grower_Number', 'Grower_Name', 'National_ID',
                    'Mobile_Number', 'District')

admin.site.register(Grower, GrowerAdmin)
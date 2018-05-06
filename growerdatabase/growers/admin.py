from django.contrib import admin

from .models import Grower, SmsQueue


class GrowerAdmin(admin.ModelAdmin):
    list_display = ('Grower_Number', 'Grower_Name', 'National_ID',
                    'Mobile_Number', 'District')


class SmsQueueAdmin(admin.ModelAdmin):
    list_display = ('cellphone', 'message', 'is_sent')


# admin.site.register(Grower, GrowerAdmin)
# admin.site.register(SmsQueue, SmsQueueAdmin)
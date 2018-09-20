from django.contrib import admin

from data_ingestion_service.models import StoredFiles


admin.site.register(StoredFiles, admin.ModelAdmin)

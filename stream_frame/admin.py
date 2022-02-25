from django.contrib import admin

from stream_frame.models import ServiceAccount


@admin.register(ServiceAccount)
class ServiceAccountAdmin(admin.ModelAdmin):
  list_display = ('name', 'modified')
  list_filter = ('modified',)

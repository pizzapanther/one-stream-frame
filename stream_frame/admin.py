from django.contrib import admin

from stream_frame.models import OAuthCredentials


@admin.register(OAuthCredentials)
class OAuthAdmin(admin.ModelAdmin):
  list_display = ('name', 'modified')
  list_filter = ('modified',)

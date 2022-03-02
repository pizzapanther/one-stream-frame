from django.contrib import admin
from django.utils.html import mark_safe

from stream_frame.models import OAuthCredentials


@admin.register(OAuthCredentials)
class OAuthAdmin(admin.ModelAdmin):
  list_display = ('name', 'modified', 'authorize')
  list_filter = ('modified',)

  def authorize(self, obj):
    if obj and not obj.token:
      return mark_safe(f'<a href="/stream-frame/start-auth/{obj.id}/">Authorize</a>')

from django.contrib import admin
from django.utils.html import mark_safe

from stream_frame.models import OAuthCredentials, Channel, VideoEmbedOn


@admin.register(OAuthCredentials)
class OAuthAdmin(admin.ModelAdmin):
  list_display = ('name', 'modified', 'authorize')
  list_filter = ('modified',)

  def authorize(self, obj):
    if obj and not obj.token and obj.client_secret:
      return mark_safe(f'<a href="/stream-frame/start-auth/{obj.id}/">Authorize</a>')


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
  list_display = ('name', 'modified')
  list_filter = ('modified',)
  raw_id_fields = ('creds',)


@admin.register(VideoEmbedOn)
class VideoAdmin(admin.ModelAdmin):
  list_display = ('video_id', 'modified')
  list_filter = ('modified',)
  search_fields = ('video_id',)

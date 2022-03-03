import time

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from django.conf import settings
from django.db import models


class OAuthCredentials(models.Model):
  name = models.CharField(max_length=70)
  token = models.JSONField(blank=True, null=True)
  client_secret = models.JSONField()

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name


class Channel(models.Model):
  name = models.CharField(max_length=70)
  channel_id = models.CharField(max_length=255)
  creds = models.ForeignKey(OAuthCredentials, on_delete=models.CASCADE)

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

  @property
  def client(self):
    if not getattr(self, '_client', None):
      creds = google.oauth2.credentials.Credentials(**self.creds.token)
      self._client = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)

    return self._client

  def find_live(self):
    resp = self.client.search().list(eventType="live", channelId=self.channel_id, part="snippet", maxResults=1, type="video").execute()
    items = resp.get('items')
    if items:
      return items[0]['id']['videoId']

  def get_video(self, vid):
    if not getattr(self, '_video', None):
      resp = self.client.videos().list(part='snippet,status,player', id=vid).execute()
      self._video = resp.get('items')[0]

    return self._video

  def allow_embed(self, vid):
    embedded = VideoEmbedOn.objects.filter(video_id=vid).first()
    if embedded:
      return embedded

    video = self.get_video(vid)

    if video['status']['embeddable']:
      embedded = VideoEmbedOn(video_id=vid)
      embedded.save()
      return embedded

    else:
      self.client.videos().update(part='status', body={"id": vid, "status": {"embeddable": True}}).execute()
      embedded = VideoEmbedOn(video_id=vid)
      embedded.save()
      time.sleep(1)
      del self._video

      return embedded

  @property
  def embed_code(self):
    template =  """<div id="stream-frame">
  <h2>Waiting for Stream to Start</h2>
</div>
<script src="{base}/stream-frame/channel_{id}.js"></script>"""

    template = template.replace('{id}', str(self.id))
    template = template.replace('{base}', settings.BASE_URL)
    return template

class VideoEmbedOn(models.Model):
  video_id = models.CharField(max_length=255, db_index=True)

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.video_id

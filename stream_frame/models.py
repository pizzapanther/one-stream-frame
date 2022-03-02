import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

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
    resp = self.client.videos().list(part='snippet,status,player', id=vid).execute()
    return resp.get('items')[0]

  def allow_embed(self, vid):
    embedded = VideoEmbedOn.objects.filter(video_id=vid).first()
    if embedded:
      return

    video = self.get_video(vid)

    if not video['status']['embeddable']:
      self.client.videos().update(part='status', body={"id": vid, "status": {"embeddable": True}}).execute()
      embedded = VideoEmbedOn(video_id=vid)
      embedded.save()
      return embedded


class VideoEmbedOn(models.Model):
  video_id = models.CharField(max_length=255, db_index=True)

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

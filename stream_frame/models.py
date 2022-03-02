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


class Channel:
  channel_id = "UCmo8zL1ZhvT4vYNzhSAuAEw"
  api_key = "AIzaSyA0ObJTTUOJreXFfLGD91p3GqpYIn02qzs"

  @property
  def service_account(self):
    return ServiceAccount.objects.all().first()

  @property
  def client(self):
    scopes = [
      "https://www.googleapis.com/auth/youtube",
      "https://www.googleapis.com/auth/youtube.readonly",
      "https://www.googleapis.com/auth/youtube.force-ssl",
      "https://www.googleapis.com/auth/youtube.upload",
    ]

    if not getattr(self, '_client', None):
      creds = service_account.Credentials.from_service_account_info(
        self.service_account.credentials, scopes=scopes, subject="paul.m.bailey@gmail.com")
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
    video = self.get_video(vid)
    print(video)

    if not video['status']['embeddable']:
      print('NARF')
      self.client.videos().update(part='status', body={"id": vid, "status": {"embeddable": True}}).execute()

    return resp

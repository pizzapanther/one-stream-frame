from django import http
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

import google.oauth2.credentials
import google_auth_oauthlib.flow

from stream_frame.models import OAuthCredentials, Channel

SCOPES = scopes = [
  "https://www.googleapis.com/auth/youtube",
  "https://www.googleapis.com/auth/youtube.readonly",
  "https://www.googleapis.com/auth/youtube.force-ssl",
  "https://www.googleapis.com/auth/youtube.upload",
]


def start_auth(request, cid):
  creds = get_object_or_404(OAuthCredentials, id=cid)

  flow = google_auth_oauthlib.flow.Flow.from_client_config(
    creds.client_secret,
    scopes=SCOPES,
  )
  flow.redirect_uri = f'{request.scheme}://{request.get_host()}/stream-frame/auth-ret/'

  authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    state=cid,
  )
  return http.HttpResponseRedirect(authorization_url)


def auth_ret(request):
  state = request.GET.get('state')
  creds = get_object_or_404(OAuthCredentials, id=state)

  flow = google_auth_oauthlib.flow.Flow.from_client_config(
    creds.client_secret,
    scopes=SCOPES,
    state=state
  )
  flow.redirect_uri = f'{request.scheme}://{request.get_host()}/stream-frame/auth-ret/'
  flow.fetch_token(authorization_response=request.build_absolute_uri())

  creds.token = {
    'token': flow.credentials.token,
    'refresh_token': flow.credentials.refresh_token,
    'token_uri': flow.credentials.token_uri,
    'client_id': flow.credentials.client_id,
    'client_secret': flow.credentials.client_secret,
    'scopes': flow.credentials.scopes,
  }
  creds.save()
  return http.HttpResponseRedirect('/admin/stream_frame/oauthcredentials/')


def channel_status(request, cid):
  channel = get_object_or_404(Channel, id=cid)
  vid = channel.find_live()

  embed = None
  status = 'offline'
  if vid:
    channel.allow_embed(vid)
    data = channel.get_video(vid)
    embed = data['player']['embedHtml']
    status = 'live'

  return http.JsonResponse({'status': status, 'embed': embed})


def channel_html(request, cid):
  channel = get_object_or_404(Channel, id=cid)
  return TemplateResponse(request, 'stream_frame/framegen.html', {'channel': channel})


def channel_js(request, cid):
  channel = get_object_or_404(Channel, id=cid)
  return TemplateResponse(request, 'stream_frame/framegen.js', {'channel': channel}, content_type="text/javascript")

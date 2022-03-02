from django import http
from django.shortcuts import render
from django.shortcuts import get_object_or_404

import google.oauth2.credentials
import google_auth_oauthlib.flow

from stream_frame.models import OAuthCredentials

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

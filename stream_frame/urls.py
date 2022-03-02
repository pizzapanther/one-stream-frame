from django.urls import path

import stream_frame.views as views


urlpatterns = [
  path('start-auth/<int:cid>/', views.start_auth),
  path('status_<int:cid>.json', views.channel_status),
  path('channel_<int:cid>.html', views.channel_html),
  path('channel_<int:cid>.js', views.channel_js),
  path('auth-ret/', views.auth_ret),
]

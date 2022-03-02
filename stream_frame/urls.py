from django.urls import path

import stream_frame.views as views


urlpatterns = [
  path('start-auth/<int:cid>/', views.start_auth),
  path('auth-ret/', views.auth_ret),
]

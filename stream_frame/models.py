from django.db import models


class ServiceAccount(models.Model):
  name = models.CharField(max_length=70)
  credentials = models.JSONField()

  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

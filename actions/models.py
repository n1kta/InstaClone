from django.db import models
from django.contrib.auth.models import User


class Action(models.Model):
    user = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )

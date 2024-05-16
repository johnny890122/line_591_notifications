from django.db import models
from django import forms
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

class RentCondition(models.Model):
    url = models.URLField() # TODO: remove this field later

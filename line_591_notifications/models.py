from django.db import models
from django import forms
import uuid

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=1000)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    rent_url = models.CharField(max_length=1000)
    
# class RentCondition(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    # url = models.URLField() # TODO: remove this field later

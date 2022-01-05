from django.db import models
from django.db.models import JSONField

class Property(models.Model):
    title = models.CharField(max_length=255, null=False)
    address = models.TextField(null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled_at = models.DateTimeField(auto_now=False, null=True)
    status = models.CharField(max_length=35, null=False)

class Activity(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    schedule = models.DateTimeField(auto_now=False, null=False)
    title = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=35, null=False)

    class Meta:
        unique_together = (('property_id', 'schedule'),)

class Survey(models.Model):
    activity_id = models.ForeignKey(Activity, on_delete=models.CASCADE)
    answers = JSONField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models

PROPERTY_STATUS = (
    ('activa', 'activa'),
    ('inactiva', 'inactiva'),
)

ACTIVITY_STATUS = (
    ('active', 'activo'),
    ('done', 'realizada'),
    ('cancel', 'cancelada')
)

class Property(models.Model):
    title = models.CharField(max_length=255, null=False)
    address = models.TextField(null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled_at = models.DateTimeField(auto_now=False, null=True)
    status = models.CharField(max_length=35, null=False, choices=PROPERTY_STATUS)

class Activity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    schedule = models.DateTimeField(auto_now=False, null=False)
    title = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=35, null=False, choices=ACTIVITY_STATUS)

    class Meta:
        unique_together = (('property', 'schedule'),)

class Survey(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE)
    answers = models.JSONField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

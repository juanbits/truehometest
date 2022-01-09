from datetime import datetime, timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from .models import *

# C nuevas create
# R listar list
# U reagendar
# D cancelar

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class PropertySerializer_List(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id', 'title', 'address')


nx = timezone.now()

class ActivitySerializer_List(serializers.HyperlinkedModelSerializer):
    property = PropertySerializer_List(many=False, read_only=True)
    condition = serializers.SerializerMethodField()
    survey = serializers.SerializerMethodField()

    def get_condition(self, obj):
        result = 'Cancelada'
        if obj.status == 'active':
            if obj.schedule >= nx:
                result = 'Pendiente a realizar'
            else:
                result = 'Atrasada'
        elif obj.status == 'done':
            result = 'Finalizada'
        return result
    
    def get_survey(self, obj):
        result = None
        survey = Survey.objects.filter(activity=obj.pk)
        if survey.exists():
            url = reverse('survey-detail', kwargs={'pk': survey.first().pk})
            result = self.context['request']._current_scheme_host + url
        return result

    class Meta:
        model = Activity
        fields = ('id', 'schedule', 'title', 'created_at', 'status', 'property', 'condition', 'survey')

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

    def create(self, validated_data):
        schedule_horaMenos = validated_data.get('schedule') - timedelta(hours=1)
        schedule_horaMas = validated_data.get('schedule') + timedelta(hours=1)
        schedule_libre = Activity.objects.filter(property = validated_data.get('property').pk ).exclude(status='cancel').filter(schedule__gt = schedule_horaMenos ).filter(schedule__lt = schedule_horaMas )

        if validated_data.get('property').status == 'inactiva':
            raise serializers.ValidationError((f"La property {validated_data.get('property').pk} esta inactiva, no se pueden crear actividades" )) 

        if len(schedule_libre) > 0:
            raise serializers.ValidationError((f"El schedule ({validated_data.get('schedule')}) no se encuentra disponible para la property ({validated_data.get('property').pk})" ))         

        return Activity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        schedule_old_time = instance.schedule.time()
        schedule_new_date = validated_data.get('schedule').date()
        validated_data['schedule'] = datetime.combine(schedule_new_date, schedule_old_time)

        for e in ['property', 'title', 'created_at', 'status']:
            validated_data.pop(e, None)
        return super().update(instance, validated_data)

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'
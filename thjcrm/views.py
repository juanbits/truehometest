import django_filters.rest_framework
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.decorators import action, permission_classes

from .models import *
from .serializers import *
from .filters import ActivityFilter

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()

    def list(self, request, *args, **kwargs):
        if len(self.request.query_params) > 0 :
            queryset = Activity.objects.all()
            queryset = ActivityFilter(data=request.GET, queryset=queryset, request=request).qs
        else:
            schedule_menos3dias = datetime.now() - timedelta(days=3)
            schedule_mas2semanas = datetime.now() + timedelta(weeks=2)
            queryset = Activity.objects.exclude(status='cancel').filter(schedule__gt = schedule_menos3dias ).filter(schedule__lt = schedule_mas2semanas )            
        
        serializer = ActivitySerializer_List(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        activity = self.get_object()
        if activity.status == 'cancel':
            return Response(data='La actividad se encuentra cancelada, no puede reagendarse.', status=400)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        activity = self.get_object()
        activity.status = 'cancel'
        activity.save()
        return Response(data='Actividad cancelada correctamente')

class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.filters import DjangoFilterBackend
from app.serializers import *
from app.models import *
from django.db import transaction
from django.utils import timezone
from django.db.models import Max
from datetime import datetime
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from app.filters import *
from app.tasks import update_active_machines

import json

# Create your views here.

class DummyView(APIView):
    def get(self, request, format=None):
        redis_publisher = RedisPublisher(facility='foobar', broadcast=True)
        message = RedisMessage('Hello World')
        # and somewhere else
        redis_publisher.publish_message(message)
        return Response(status=status.HTTP_200_OK)


class MachineListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Machine.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_class = MachineFilter
    serializer_class = MachineSerializer

class MachineDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    def perform_update(self, serializer):
        serializer.save(active=True)

class MachinePeriodicView(APIView):
    def post(self, request, pk, format=None):
        pk = int(pk)
        user_info = json.loads(request.data["user_info"])
        machine_info = json.loads(request.data["machine_info"])


        try:
            with transaction.atomic():
                m = Machine.objects.select_for_update().get(pk=pk)
                if m.ip_address!=machine_info["ip_address"]:
                    a = Alert(alert_type=1, text="IP Address of "+m.host_name+" has been changed.")
                    a.save()

                serializer = MachineSerializer(m, machine_info, partial=True)

                if serializer.is_valid():
                    serializer.save(active=True, last_active_at=timezone.now())
                else:
                    print serializer.errors

                for currentUser in user_info["all_user_details"]:

                    curr_user, created = MachineUser.objects.get_or_create(username=currentUser["username"], defaults={"name":currentUser["username"]})

                    mls, created = MachineLoginSession.objects.get_or_create(machine=m, user=curr_user, login_time=currentUser["logged_in_at"], ip_address=currentUser["ip_address"])

                    als, created = ActiveLoginSession.objects.get_or_create(mls=mls, machine=m, user=curr_user, login_time=currentUser["logged_in_at"], ip_address=currentUser["ip_address"])                    

                return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class CINManUserListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = CINManUser.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_class = CINManUserFilter
    serializer_class = CINManUserSerializer

class CINManUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = CINManUser.objects.all()
    serializer_class = CINManUserSerializer

class MachineUserListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MachineUser.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_class = MachineUserFilter
    serializer_class = MachineUserSerializer

class MachineUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MachineUser.objects.all()
    serializer_class = MachineUserSerializer

class MachineLoginSessionListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MachineLoginSession.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_class = MachineLoginSessionFilter
    serializer_class = MachineLoginSessionSerializer

class MachineLoginSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MachineLoginSession.objects.all()
    serializer_class = MachineLoginSessionSerializer

class LogEntryListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = LogEntry.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_class = LogEntryFilter
    serializer_class = LogEntrySerializer

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user.machineuser_profile)

class LogEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer

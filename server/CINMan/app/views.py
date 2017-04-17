from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.filters import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
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
    serializer_class = MachineListSerializer

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
                currentUser = user_info["current_user"]
                curr_user, created = MachineUser.objects.get_or_create(username=currentUser["username"], defaults={"name":currentUser["username"]})

                m = Machine.objects.select_for_update().get(pk=pk)
                if m.ip_address!=machine_info["ip_address"]:
                    a = Alert(alert_type=1, user=curr_user, text="IP Address of "+m.host_name+" has been changed.")
                    a.save()
                    a.machines.add(m)

                serializer = MachineSerializer(m, machine_info, partial=True)

                if serializer.is_valid():
                    x = serializer.save(active=True, last_active_at=timezone.now())
                else:
                    print serializer.errors

                userhash = set()

                for currentUser in user_info["all_user_details"]:

                    curr_user, created = MachineUser.objects.get_or_create(username=currentUser["username"], defaults={"name":currentUser["username"]})

                    mls, created = MachineLoginSession.objects.get_or_create(machine=m, user=curr_user, login_time=currentUser["logged_in_at"], ip_address=currentUser["ip_address"], tty=currentUser["tty"])

                    als, created = ActiveLoginSession.objects.get_or_create(mls=mls, machine=m, user=curr_user, login_time=currentUser["logged_in_at"], ip_address=currentUser["ip_address"], tty=currentUser["tty"], defaults={"username":curr_user.username})

                    userhash.add(curr_user.username+"|"+str(mls.login_time)+"|"+als.tty)

                for als in ActiveLoginSession.objects.filter(machine=m):
                    if (als.user.username+"|"+str(als.mls.login_time)+"|"+als.tty) not in userhash:
                        als.mls.logout_time = timezone.now()
                        currUser = als.user
                        als.delete()
                        if currUser.active_login_sessions.count()==0:
                            currUser.currently_logged = False
                            currUser.save(update_fields=['currently_logged'])

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

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 80

class AlertListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Alert.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = AlertFilter
    serializer_class = AlertSerializer

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
        obj = serializer.save()
        obj.user = MachineUser.objects.get(username=self.request.data["username"])
        obj.save()
        a = json.loads(obj.text)
        if a["event"]=="usb_connect":
            alert = Alert(log_entry=obj,alert_type=2,user=obj.user,text="USB Connected")
        elif a["event"]=="package_install":
            alert = Alert(log_entry=obj,alert_type=1,user=obj.user,text="Package Installed")
        elif a["event"]=="package_remove":
            alert = Alert(log_entry=obj,alert_type=1,user=obj.user,text="Package Removed")
        elif a["event"]=="usb_disconnect":
            alert = Alert(log_entry=obj,alert_type=1,user=obj.user,text="USB Disconnected")
        elif a["event"]=="auth_failure":
            alert = Alert(log_entry=obj,alert_type=1,user=obj.user,text="Failed Authorization")
        elif a["event"]=="sudo_access":
            alert = Alert(log_entry=obj,alert_type=1,user=obj.user,text="SUDO Access Attempted")
        elif a["event"]=="incorrect_password":
            alert = Alert(log_entry=obj,alert_type=1,user=obj.user,text="Incorrect Password")

        alert.save()
        alert.machines.add(obj.machine)


class LogEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer

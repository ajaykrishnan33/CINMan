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

class MachineActivateView(APIView):
    def post(self, request, pk, format=None):
        pk = int(pk)
        try:
            with transaction.atomic():
                m = Machine.objects.select_for_update().get(pk=pk)
                m.active = True
                m.save()
                return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class MachineDeactivateView(APIView):
    def post(self, request, pk, format=None):
        pk = int(pk)
        try:
            with transaction.atomic():
                m = Machine.objects.select_for_update().get(pk=pk)
                m.active = False
                m.save()
                return Response(status=status.HTTP_200_OK)
        except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

class MachineLoginView(APIView):
    def post(self, request, pk, format=None):
            pk = int(pk)
        # try:
            with transaction.atomic():
                u = MachineUser.objects.select_for_update().get(username=request.data["user"])
                m = Machine.objects.get(pk=pk)
                login_time = datetime.fromtimestamp(float(request.data["login_time"]))
                mls, created = MachineLoginSession.objects.get_or_create(machine=m, user=u, login_time=login_time)

                if not created:
                    return Response(status=status.HTTP_200_OK)

                u.currently_logged = True
                u.last_logged_in_machine = m
                u.last_logged_in_date = login_time
                u.number_of_simultaneous_logins += 1

                u.save()

                # if u.number_of_simultaneous_logins>1:
                #   take action

                return Response(status=status.HTTP_200_OK)
        # except:
        #   return Response(status=status.HTTP_400_BAD_REQUEST)

class MachineLogoutView(APIView):
    def post(self, request, pk, format=None):
        pk = int(pk)
        try:
            with transaction.atomic():
                u = MachineUser.objects.select_for_update().get(username=request.data["user"])
                login_time = datetime.fromtimestamp(float(request.data["login_time"]))
                m = Machine.objects.get(pk=pk)
                mls = MachineLoginSession.objects.get(machine=m, user=u, login_time=login_time, logout_time=None)
                mls.logout_time = datetime.fromtimestamp(float(request.data["logout_time"]))
                mls.save()

                u.number_of_simultaneous_logins -= 1
                if u.number_of_simultaneous_logins == 0:
                    u.currently_logged = False
                u.save()

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

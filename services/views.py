"""
Views for the REST API.
"""

__author__ = 'Phil Ratcliffe'

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Service
from .serializer import ServiceSerializer


@api_view(['GET', 'POST'])
def list_or_add(request):
    """
    List all services or create a services record.
    """
    if request.method == 'GET':
        queryset = Service.objects.all()
        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data.copy()
            data.update({'change': 'created'})
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            # TBD: This response is not currently in the features doc
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def find_or_delete(request, service, version=None):
    """
    Finds a service or deletes all versions of a service.
    """
    if request.method == 'GET':
        data = {'service': service}
        queryset = Service.objects.filter(service=service)
        if version is not None:
            queryset = queryset.filter(version=version)
            data['version'] = version
        data['count'] = queryset.count()
        return Response(data, status.HTTP_200_OK)

    elif request.method == 'DELETE':
        queryset = Service.objects.filter(service=service)

        if queryset:
            queryset.delete()
            data = {'service': service, 'change': 'removed'}
            return Response(data, status.HTTP_204_NO_CONTENT)

        data = {'error': 'not found'}
        return Response(data, status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update(request, pk):
    """
    Updates a service.

    TODO: Include pk in returned data so client can use it for updates.
    Update features file to reflect this.
    """
    service = get_object_or_404(Service, pk=pk)
    serializer = ServiceSerializer(service, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'change': 'changed'}, status.HTTP_200_OK)
    else:
        # TBD: This response is not currently in the features doc
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

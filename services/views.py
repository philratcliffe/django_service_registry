from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Service
from .serializer import ServiceSerializer


@api_view(['GET', 'POST'])
def service_list(request, service=None, version=None):
    """
    List all services, or create a new task.
    """
    if request.method == 'GET':
        name = request.query_params.get('name', None)
        name = request.query_params.get('version', None)
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        name = request.POST.get('name', None)
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

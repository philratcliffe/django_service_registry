from django.urls import path

from . import views

urlpatterns = [
    path('v1', views.list_or_add, name='list_or_add_endpoint'),
    path('v1/<int:pk>', views.update, name='update_endpoint'),
    path('v1/<service>', views.find_or_delete, name='find_or_delete_endpoint'),
    path(
        'v1/<service>/<version>',
        views.find_or_delete,
        name='find_or_delete_endpoint'),
]

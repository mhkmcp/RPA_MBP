# Create your views here.
from django_celery_results.models import TaskResult
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from bots.tasks import worker_bot_process, nid_bot_process


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def worker_bot(request):
    if request.method == 'GET':
        worker_bot_process.delay()

    return Response({"status": True}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def nid_bot(request):
    if request.method == 'GET':
        print("executing nid bot")
        nid_bot_process.delay()

    return Response({"status": True}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def bot_status(request):
    if request.method == 'GET':
        status_dict = dict()
        result = TaskResult.objects.all()
        process_count = result.count()
        success = result.filter(status='SUCCESS').count()
        percentage = (success / process_count)*100

        status_dict['process_count'] = process_count
        status_dict['success'] = success
        status_dict['percentage'] = int(percentage)

    return Response(status_dict, status=status.HTTP_200_OK)

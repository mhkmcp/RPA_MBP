# Create your views here.
from django.http import HttpResponseRedirect
from django_celery_results.models import TaskResult
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from bots.forms import EmailConfigForm, NidConfigForm, CbsConfigForm
from bots.models import BotConfig, BotConfigNid, BotConfigCbs
from bots.tasks import worker_bot_process, nid_bot_process


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def worker_bot(request):
    if request.method == 'GET':
        task = worker_bot_process.delay()

        print(task.id)

        return Response({"task_id": task.id}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def nid_bot(request):
    if request.method == 'GET':
        print("executing nid bot")
        task = nid_bot_process.delay()

        return Response({"task_id": task.id}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def bot_status(request):
    if request.method == 'GET':
        status_dict = dict()
        result = TaskResult.objects.all()
        process_count = result.count()
        success = result.filter(status='SUCCESS').count()
        percentage = (success / process_count) * 100

        status_dict['process_count'] = process_count
        status_dict['success'] = success
        status_dict['percentage'] = int(percentage)

        return Response(status_dict, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.AllowAny,))
def process_queue_status(request, t_id):
    print(repr(request))
    if request.method == 'GET':
        print("post hit")
        status_dict = dict()

        data = t_id
        # data = request.query_params.get('t_data', None)
        # data = request.data
        print(t_id)

        try:
            task = TaskResult.objects.get(task_id=data)
            print(task.task_name)

            if task.status == 'SUCCESS':
                status_dict['status'] = True
            else:
                status_dict['status'] = False

        except TaskResult.DoesNotExist:
            status_dict['status'] = False

        return Response(status_dict, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((permissions.AllowAny,))
def process_queue_status_worker(request, t_id):
    print(repr(request))
    if request.method == 'GET':
        print("post hit")
        status_dict = dict()

        data = t_id
        # data = request.query_params.get('t_data', None)
        # data = request.data
        print(t_id)

        try:
            task = TaskResult.objects.get(task_id=data)
            print(task.task_name)

            if task.status == 'SUCCESS':
                status_dict['status'] = True
            else:
                status_dict['status'] = False

        except TaskResult.DoesNotExist:
            status_dict['status'] = False

        return Response(status_dict, status=status.HTTP_200_OK)


def email_settings_update(request):
    if request.method == 'POST':
        form = EmailConfigForm(request.POST)

        if form.is_valid():
            try:
                older_email_config = BotConfig.objects.get(config_validity=True, config_class="email_results")
                older_email_config.config_validity = False
                older_email_config.save()

                new_email_config = BotConfig()
                new_email_config.config_settings = form.cleaned_data['email_config']
                new_email_config.config_class = "email_results"

                new_email_config.save()
            except BotConfig.DoesNotExist:
                new_email_config = BotConfig()
                new_email_config.config_settings = form.cleaned_data['email_config']
                new_email_config.config_class = "email_results"

                new_email_config.save()

        return HttpResponseRedirect('/dashboard/settings/')


def nid_settings_update(request):
    if request.method == 'POST':
        form = NidConfigForm(request.POST)

        if form.is_valid():
            try:
                old_setting = BotConfigNid.objects.get(config_validity=True)
                old_setting.config_validity = False
                old_setting.save()

                new_setting = BotConfigNid()
                new_setting.nid_url = form.cleaned_data['nid_url']
                new_setting.nid_username = form.cleaned_data['nid_username']
                new_setting.nid_password = form.cleaned_data['nid_password']
                new_setting.save()

            except BotConfigNid.DoesNotExist:
                new_setting = BotConfigNid()
                new_setting.nid_url = form.cleaned_data['nid_url']
                new_setting.nid_username = form.cleaned_data['nid_username']
                new_setting.nid_password = form.cleaned_data['nid_password']
                new_setting.save()

        return HttpResponseRedirect('/dashboard/settings/')


def cbs_settings_update(request):
    if request.method == 'POST':
        form = CbsConfigForm(request.POST)

        if form.is_valid():
            try:
                old_setting = BotConfigCbs.objects.get(config_validity=True)
                old_setting.config_validity = False
                old_setting.save()

                new_setting = BotConfigCbs()
                new_setting.cbs_url = form.cleaned_data['cbs_url']
                new_setting.cbs_username = form.cleaned_data['cbs_username']
                new_setting.cbs_password = form.cleaned_data['cbs_password']
                new_setting.save()

            except BotConfigCbs.DoesNotExist:
                new_setting = BotConfigCbs()
                new_setting.cbs_url = form.cleaned_data['cbs_url']
                new_setting.cbs_username = form.cleaned_data['cbs_username']
                new_setting.cbs_password = form.cleaned_data['cbs_password']
                new_setting.save()

        return HttpResponseRedirect('/dashboard/settings/')

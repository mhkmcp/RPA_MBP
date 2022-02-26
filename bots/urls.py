from django.conf.urls import url

from bots.views import worker_bot, nid_bot, bot_status, process_queue_status, process_queue_status_worker, \
    email_settings_update, nid_settings_update, cbs_settings_update


urlpatterns = [
    url(r'^worker/', worker_bot),
    url(r'^nid/', nid_bot),
    url(r'^status/', bot_status),
    url(r'^process-status-nid/(?P<t_id>[-\w]+)/', process_queue_status),
    url(r'^process-status-worker/(?P<t_id>[-\w]+)/', process_queue_status_worker),
    url(r'^settings/report-email/', email_settings_update),
    url(r'^settings/nid/', nid_settings_update),
    url(r'^settings/cbs/', cbs_settings_update),

]

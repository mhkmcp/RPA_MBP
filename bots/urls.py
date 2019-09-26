from django.conf.urls import url


from bots.views import worker_bot, nid_bot, bot_status

urlpatterns = [
    url(r'^worker/', worker_bot),
    url(r'^nid/', nid_bot),
    url(r'^status/', bot_status),
]

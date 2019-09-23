from django.conf.urls import url


from bots.views import worker_bot, nid_bot

urlpatterns = [
    url(r'^worker/', worker_bot),
    url(r'^nid/', nid_bot),
]

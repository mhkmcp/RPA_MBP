
from django.conf.urls import url

from dashboard.views import render_landing_page

urlpatterns = [
                  url(r'^bankasia/', render_landing_page, name='dashboard_landing_page'),

              ]
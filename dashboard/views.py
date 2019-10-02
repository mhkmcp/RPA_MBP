from django.shortcuts import render, redirect

# Create your views here.
from bots.models import BotConfig, BotConfigNid, BotConfigCbs


def render_landing_page(request):
    page_title = 'Dashboard | FernTech AIW'
    navbar_title = 'Overview'

    if request.user.is_authenticated:
        return render(request, 'dashboard/landing.html', {
            'page_title': page_title,
            'navbar_title': navbar_title,

        })
    else:
        return redirect('/login/')


def render_settings_page(request):
    page_title = 'Dashboard | FernTech AIW'
    navbar_title = 'Settings'
    try:
        email_config = BotConfig.objects.get(config_validity=True, config_class="email_results")
    except BotConfig.DoesNotExist:
        email_config = None
    try:
        nid_config = BotConfigNid.objects.get(config_validity=True)
    except BotConfigNid.DoesNotExist:
        nid_config = None
    try:
        cbs_config = BotConfigCbs.objects.get(config_validity=True)
    except BotConfigCbs.DoesNotExist:
        cbs_config = None

    if request.user.is_authenticated:
        return render(request, 'dashboard/settings.html', {
            'page_title': page_title,
            'navbar_title': navbar_title,
            'email_config': email_config,
            'nid_config': nid_config,
            'cbs_config': cbs_config,
        })
    else:
        return redirect('/login/')


def homepage_redirection(request):
    if request.user.is_authenticated:
        return redirect('dashboard_landing_page')
    else:
        return redirect('/login')

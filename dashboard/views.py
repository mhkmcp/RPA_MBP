from django.shortcuts import render, redirect


# Create your views here.


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


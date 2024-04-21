from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from float.forms import FloatArea


def page_not_found(request, exception):
    return HttpResponseNotFound('Page not found')


def main_page(request):
    t = render_to_string('main.html')
    return HttpResponse(t)


def monitoring_page(request):
    if request.method == 'POST':
        form = FloatArea(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = FloatArea()
    # t = render_to_string('monitoring.html')
    return render(request, 'monitoring.html', {'form': form})


def parsing_page(request):
    if request.method == 'POST':
        form = FloatArea(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = FloatArea()
    # t = render_to_string('monitoring.html')
    return render(request, 'monitoring.html', {'form': form})
    # return HttpResponse("Start to parsing!")


def profile_page(request):
    if request.GET['id']:
        return HttpResponse(f"Profile user with number {request.GET['id']}")
    else:
        raise Http404("Profile not found")


def calculator_page(request):
    return HttpResponse("Start to calculator!")


def register_page(request):
    return HttpResponse("Register page!")


def login_page(request):
    return HttpResponse("Login page!")

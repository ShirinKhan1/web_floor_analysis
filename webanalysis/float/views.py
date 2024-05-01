from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from float.forms import *
import datetime
from func.parse_floats import parse_links
from func.monitoring import streaming


def page_not_found(request, exception):
    return HttpResponseNotFound('Page not found')


def main_page(request):
    # t = render_to_string('main.html')
    return render(request, 'main.html')


def monitoring_page(request):
    if request.method == 'POST':
        form = FloatArea(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            args = {
                'url': form.cleaned_data['link'],
                'datetimedttm': datetime.datetime.now(),
                'user_id': request.POST['user_id'],
                'method': request.POST['method'],
                'finish': float(request.POST['minutes'])
            }
            print(args)
            streaming(url=args['url'], method=args['method'], user_id=args['user_id'],
                      datetimedttm=args['datetimedttm'], finish=args['finish'])
    else:
        form = FloatArea()
        # t = render_to_string('monitoring.html')
    return render(request, 'monitoring.html', {'form': form})
    # return HttpResponse("Start to parsing!")


def parsing_page(request):
    if request.method == 'POST':
        form = FloatArea(request.POST)
        if form.is_valid():
            args = {
                'url':  form.cleaned_data['link'],
                'datetimedttm': datetime.datetime.now(),
                'user_id': request.POST['user_id'],
                'method': request.POST['method']
            }
            print(args)
            parse_links(url=args['url'], method=args['method'],
                        user_id=args['user_id'], datetimedttm=args['datetimedttm'])
    else:
        form = FloatArea()
    # t = render_to_string('monitoring.html')
    return render(request, 'parsing.html', {'form': form})
    # return HttpResponse("Start to parsing!")


def profile_page(request):
    if request.GET['id']:
        return HttpResponse(f"Profile user with number {request.GET['id']}")
    else:
        raise Http404("Profile not found")


def calculator_page(request):
    if request.method == 'POST':
        form = Ai_calc(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = Ai_calc()
    # t = render_to_string('monitoring.html')
    return render(request, 'calculator.html', {'form': form})


def register_page(request):
    return HttpResponse("Register page!")


def login_page(request):
    return HttpResponse("Login page!")

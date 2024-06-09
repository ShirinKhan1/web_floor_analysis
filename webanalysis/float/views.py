import pandas as pd
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
# from django.template.loader import render_to_string
from float.forms import *
import datetime

from func.get_geopandas import get_geopandas
from func.parse_floats import parse_links
from func.monitoring import streaming
from func.estate_analysis import payback, statistic_district
import plotly.express as px
import plotly.io as pio
# from float.tasks import parse_links_task, hello


def page_not_found(request, exception):
    return HttpResponseNotFound('Page not found')


def main_page(request):
    # t = render_to_string('main.html')
    graph = get_geopandas()
    return render(request, 'main.html', {'graph': graph})


def monitoring_page(request):
    if not request.user.is_authenticated:
        return render(request, 'not_auth.html')
    else:
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
    if not request.user.is_authenticated:
        return render(request, 'not_auth.html')
    if request.method == 'POST':
        form = FloatArea(request.POST)
        if form.is_valid():
            args = {
                'url': form.cleaned_data['link'],
                'datetimedttm': datetime.datetime.now(),
                'user_id': request.POST['user_id'],
                'method': request.POST['method']
            }
            # print(args)
            # result = hello.delay()
            # result = parse_links_task.delay(args['url'], args['method'], args['user_id'], args['datetimedttm'])
            parse_links(args['url'], args['method'], args['user_id'], args['datetimedttm'])
            # print(hello())
    else:
        form = FloatArea()
    # t = render_to_string('monitoring.html')
    return render(request, 'parsing.html', {'form': form})
    # return HttpResponse("Start to parsing!")


def calculator_page(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return render(request, 'not_auth.html')
    if request.method == 'POST':
        form = Ai_calc(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = Ai_calc()
    # t = render_to_string('monitoring.html')
    return render(request, 'calculator.html', {'form': form})


def analysis_district(request):
    if not request.user.is_authenticated:
        return render(request, 'not_auth.html')
    if request.method == 'GET':
        return render(request, 'analysis.html')
    elif request.method == 'POST':
        print(request.POST)
        try:
            df, city, district = payback(request.POST['city'], request.POST['district'])
            col_gr = ['Цена продажи', 'Кол-во комнат', 'Общая площадь']
            fig = px.scatter(df, x=col_gr[1], y=col_gr[0], color=col_gr[2],
                             # labels={'cntroom': 'Количество комнат', 'price2': 'Цена', 'totalarea': 'Общая площадь'},
                             title='Зависимость цены от количества комнат и общей площади')
            graph_html = pio.to_html(fig, full_html=False)

            # Конвертация графика в HTML
            graph_html = pio.to_html(fig, full_html=False)
            return render(request, 'get_payback.html',
                          {'columns': df.columns,
                           'rows': df.values,
                           'city': city, 'district': district, 'graph': graph_html})
        except Exception as e:
            print(e)
            return render(request, 'analysis.html')


def check_district(request):
    if not request.user.is_authenticated:
        return render(request, 'not_auth.html')
    if request.method == 'GET':
        return render(request, 'checking.html')
    elif request.method == 'POST':
        print(request.POST)
        try:
            rows, columns, city, df = statistic_district(request.POST['city'])
            fig = px.box(df, x='Кол-во комнат', y='Цена продажи', points="all")
            graph_html = pio.to_html(fig, full_html=False)
            return render(request, 'get_checking.html',
                          {'columns': columns, 'rows': rows, 'city': city, 'graph': graph_html})
        except Exception as e:
            print(e)
            return render(request, 'checking.html')

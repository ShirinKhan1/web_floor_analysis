import json
import re

FILE_NAME = 'parse1'
args = ['Тип жилья',
        'Общая площадь',
        'Жилая площадь',
        'Площадь кухни',
        'Высота потолков',
        'Санузел',
        'Отделка',
        'Вид из окон',
        'Ремонт',
        'Балкон/лоджия',
        ]

args_house = [
    'Количество лифтов',
    'Тип дома',
    'Парковка',
    'Отопление',
    'Мусоропровод',
    'Год постройки',
    'Газоснабжение',
]


def del_dif(string):
    return re.sub(r'[^\u0400-\u04FF0-9, ]+', '', string)


def del_dif_2(string):
    return re.sub(r'[^\d,]+', '', string)


def fix_data_after_parsing(data_float: dict) -> dict:
    new_data = None
    # with open(link_float + '.json', 'r', encoding='utf-8') as file:
    #     existing_data = json.load(file)

        # row = existing_data[20]
        # print(test_row['price_info'])
        # for row_number in range(len(existing_data)):
    data_float['name'] = data_float['name'].replace(' м²', '')
    for i in range(len(data_float['price_info'])):
        if 'Условия сделки' in data_float['price_info'][i]:
            data_float['price_info'][i] = ['Условия сделки', data_float['price_info'][i][len('Условия сделки'):]]
        elif 'Ипотекавозможна' == data_float['price_info'][i]:
            data_float['price_info'][i] = ['Ипотека', 'Возможна']

    data_float['floor'] = [int(num) for num in data_float['floor'][len('Этаж'):].split(' из ')]

    for i in range(len(data_float['float'])):
        for arg in args:
            if arg in data_float['float'][i]:
                data_float['float'][i] = [arg, del_dif(data_float['float'][i][len(arg):])]
                if 'площадь' in data_float['float'][i][0].lower() or 'высота' in data_float['float'][i][0].lower():
                    data_float['float'][i][1] = float(del_dif_2(data_float['float'][i][1]).replace(',', '.'))
                break
    # print(test_row['house'])

    for i in range(len(data_float['house'])):
        for arg in args_house:
            if arg in data_float['house'][i]:
                data_float['house'][i] = [arg, del_dif(data_float['house'][i][len(arg):])]
                # if 'Количество лифтов' in test_row['house'][i][0]:
                #     test_row['house'][i] = test_row['house'][i][1].split(',')
                break
    # new_data = existing_data
    return data_float


def check_new_col(data):
    for row in data:
        for k in row['house']:
            if isinstance(k, str):
                print('house-', k)
        for k in row['float']:
            if isinstance(k, str):
                print('float-', k)


def write_new_data(new_data, filename=FILE_NAME):
    with open(FILE_NAME + '_fixed' + '.json', 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)
    print('Done!')


if __name__ == '__main__':
    write_new_data(fix_data_after_parsing(FILE_NAME), FILE_NAME)
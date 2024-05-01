import json
import re

FILE_NAME = 'parse1'
args = {'Тип жилья': 'typeofhousing',
        'Общая площадь': 'totalarea',
        'Жилая площадь': 'livingarea',
        'Площадь кухни': 'kitchenarea',
        'Высота потолков': 'ceiling',
        'Санузел': 'lavatory',
        'Отделка': 'finishing',
        'Вид из окон': 'window',
        'Ремонт': 'repair',
        'Балкон/лоджия': 'balkonlodge',
        }

args_house = {
    'Количество лифтов': 'elevator',
    'Тип дома': 'typeofhouse',
    'Парковка': 'parking',
    'Отопление': 'heating',
    'Мусоропровод': 'garbage',
    'Год постройки': 'year',
    'Газоснабжение': 'gas',
}


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
            data_float['price_info'][i] = ['deal', data_float['price_info'][i][len('Условия сделки'):]]
        elif 'Ипотекавозможна' == data_float['price_info'][i]:
            data_float['price_info'][i] = ['credit', 'Возможна']
        elif 'Цена за метр ' in data_float['price_info'][i]:
            data_float['price_info'][i] = ['price2', int(data_float['price_info'][i][1])]

    data_float['floor'] = [int(num) for num in data_float['floor'][len('Этаж'):].split(' из ')]
    data_float['maxfloor'] = max(data_float['floor'])
    data_float['floor'] = min(data_float['floor'])

    for i in range(len(data_float['float'])):
        for arg in args.keys():
            if arg in data_float['float'][i]:
                data_float['float'][i] = [args[arg], del_dif(data_float['float'][i][len(arg):])]
                if 'area' in data_float['float'][i][0].lower() or 'ceiling' in data_float['float'][i][0].lower():
                    data_float['float'][i][1] = float(del_dif_2(data_float['float'][i][1]).replace(',', '.'))
                break
    # print(test_row['house'])

    for i in range(len(data_float['house'])):
        for arg in args_house.keys():
            if arg in data_float['house'][i]:
                data_float['house'][i] = [args_house[arg], del_dif(data_float['house'][i][len(arg):])]
                # if 'Количество лифтов' in test_row['house'][i][0]:
                #     test_row['house'][i] = test_row['house'][i][1].split(',')
                break
            if 'year' in data_float['house'][i][0]:
                data_float['float'][i][1] = int(data_float['float'][i][1])
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

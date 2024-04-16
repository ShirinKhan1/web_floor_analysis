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
        'Газоснабжение',
        'Балкон/лоджия',
        ]

args_house = [
    'Количество лифтов',
    'Тип дома',
    'Парковка',
    'Тип перекрытий',
    'Подъезды',
    'Отопление',
    'Аварийность',
    'Строительная серия',
    'Мусоропровод',
    'Год постройки',
    'Газоснабжение'

]


def del_dif(string):
    return re.sub(r'[^\u0400-\u04FF0-9, ]+', '', string)


def del_dif_2(string):
    return re.sub(r'[^\d,]+', '', string)


def fix_data_after_parsing(filename=FILE_NAME):
    new_data = None
    with open(filename + '.json', 'r', encoding='utf-8') as file:
        existing_data = json.load(file)

        # row = existing_data[20]
        # print(test_row['price_info'])
        for row_number in range(len(existing_data)):
            row = existing_data[row_number]
            row['name'] = row['name'].replace(' м²', '')
            for i in range(len(row['price_info'])):
                if 'Условия сделки' in row['price_info'][i]:
                    row['price_info'][i] = ['Условия сделки', row['price_info'][i][len('Условия сделки'):]]
                elif 'Ипотекавозможна' == row['price_info'][i]:
                    row['price_info'][i] = ['Ипотека', 'Возможна']

            row['floor'] = [int(num) for num in row['floor'][len('Этаж'):].split(' из ')]

            for i in range(len(row['float'])):
                for arg in args:
                    if arg in row['float'][i]:
                        row['float'][i] = [arg, del_dif(row['float'][i][len(arg):])]
                        if 'площадь' in row['float'][i][0].lower() or 'высота' in row['float'][i][0].lower():
                            row['float'][i][1] = float(del_dif_2(row['float'][i][1]).replace(',', '.'))
                        break
            # print(test_row['house'])

            for i in range(len(row['house'])):
                for arg in args_house:
                    if arg in row['house'][i]:
                        row['house'][i] = [arg, del_dif(row['house'][i][len(arg):])]
                        # if 'Количество лифтов' in test_row['house'][i][0]:
                        #     test_row['house'][i] = test_row['house'][i][1].split(',')
                        break
        new_data = existing_data
    return new_data


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
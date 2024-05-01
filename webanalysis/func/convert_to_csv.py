import json
import pandas as pd

FILE_NAME = 'parse1_fixed.json'
file_to_csv = 'parse1_fixed.csv'
file_link_photo = 'photo_links.json'


def final_fix(data_float):
    properties = set()
    fixed_data = []
    # with (open(FILE_NAME, 'r', encoding='utf-8') as file):
    # existing_data = json.load(file)
    # print(existing_data[0]['price_info'])
    props = [
        'price_info',
        'float',
        'house'
    ]
    # for row in existing_data:
    for p in props:
        for n_key in range(len(data_float[p])):
            key = data_float[p][n_key][0]
            value = data_float[p][n_key][1]
            if len(key) > 3:
                data_float[key] = value
        # print(existing_data[0]['price_info'][n_key][0])
        data_float.pop(p)

    properties |= set(data_float.keys())
    fixed_data.append(data_float)
    # print(fixed_data[0])
    properties = list(properties)
    # print(properties)
    properties = list(properties)
    properties.pop(properties.index('photos'))
    return pd.DataFrame(fixed_data, columns=properties)
    # df.to_csv(file_to_csv)

# photo_link = []
# for data_float in fixed_data:
#     photo_link.append({'link': data_float['link'], 'photos': data_float['photos']})
# # def write_new_data(new_data, filename=FILE_NAME):
# with open(file_link_photo, 'w', encoding='utf-8') as file:
#     json.dump(photo_link, file, ensure_ascii=False, indent=4)
# print('Done!')

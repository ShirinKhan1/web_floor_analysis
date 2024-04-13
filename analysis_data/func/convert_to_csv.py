import json
from fix_data_after_parsing import args, args_house
FILE_NAME = 'parse1_fixed.json'
properties = set()
fixed_data = []
with (open(FILE_NAME, 'r', encoding='utf-8') as file):
    existing_data = json.load(file)
    # print(existing_data[0]['price_info'])
    props = [
        'price_info',
        'float',
        'house'
    ]
    for row in existing_data:
        for p in props:
            for n_key in range(len(row[p])):
                key = row[p][n_key][0]
                value = row[p][n_key][1]

                row[key] = value
            # print(existing_data[0]['price_info'][n_key][0])
            row.pop(p)

        properties |= set(row.keys())
        fixed_data.append(row)
    print(fixed_data)

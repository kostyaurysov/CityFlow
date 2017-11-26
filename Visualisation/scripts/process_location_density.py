import csv
from random import randint
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--csv', required=True, help='path to csv')
parser.add_argument('--out', required=True, help='output folder')

args = parser.parse_args()

class_mapping = {
    'I':'1',
    'II':'2',
    'III':'3',
    'KA1':'1',
    'KA2':'2',
    'KA3':'3',
    'KB1':'1',
    'KB2':'2',
    'KB3':'3',
    'H1':'1',
    'H2':'2',
    'H3':'3',
}

pred_class_mapping = {
    '1':'3',
    '2':'2',
    '3':'1'
}

with open(args.csv, 'r') as csvfile, open(os.path.join(args.out, 'bins.js'), 'w+') as jsfile:
    reader = csv.reader(csvfile, delimiter=',')

    bins = []

    js_content = []

    for row in reader:
        # Get GPS position
        # bin_gps = row[0:2]
        # bin_density = randint(200, 2000)

        # result = bin_gps
        # result.append(bin_density)
        # print(row)
        row[2] = class_mapping[row[2]]
        row[4] = pred_class_mapping[row[4]]
        js_content.append("\t[{},{},'{}','{}',{},{}]".format(*row))


        # bins.append((bin_gps[1:-1], volume, bin_type))
    jsfile.write('bin_locations = [\n{}\n]'.format(',\n'.join(js_content)))

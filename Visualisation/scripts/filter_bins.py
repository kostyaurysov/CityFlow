import csv
from geopy.distance import great_circle
import requests
import json
import time

def parse_point(string):
    tokens = string.split(' ')
    print(tokens)
    return float(tokens[1][1:]), float(tokens[2][:-1])

def convert_to_gps(point):
    request_string = "https://epsg.io/trans?x={}&y={}&s_srs=3879&t_srs=4326".format(point[0], point[1])
    print(request_string)
    # inp = urllib.request.urlopen(request_string).read()
    # import requests
    r = requests.get(request_string)
    data = json.loads(r.content)
    # print(data)

    return data['y'], data['x']

# convert_to_gps((25504118.695974, 6678547.805588))
#
# import sys
# sys.exit(0)

start_after = 'ylre_katuosat_point.5065'
should_begin = False


with open('bins.csv', 'r') as csvfile, open('bins_gps.csv', 'w+') as csvoutput:
     reader = csv.reader(csvfile, delimiter=';')
     spamwriter = csv.writer(csvoutput, delimiter=';')
     ID = 0

     Helsinki = (60.1699, 24.9384)

     for row in reader:
         if row[0] == start_after and not should_begin:
             should_begin = True
             continue

         if not should_begin:
             continue



         if row[5] == 'Jäteastiat' and (row[7].startswith('HKR') or row[7].startswith('(Vali')):
            print(ID)
            ID += 1
            print( ', '.join(row))
            # print(Helsinki, parse_point(row[1]))

            gps_coords = convert_to_gps(parse_point(row[1]))

            row.append('({}, {})'.format(gps_coords[0], gps_coords[1]))

            spamwriter.writerow(row)
            print(row)
            print('Sleeping...')
            time.sleep(0.5)

             # https://epsg.io/trans?x=25502640.4658732&y=6679976.55133542&s_srs=3879&t_srs=4326&callback=_callbacks_._3jafgkuzz
             # print(great_circle(Helsinki, parse_point(row[1])).meters)

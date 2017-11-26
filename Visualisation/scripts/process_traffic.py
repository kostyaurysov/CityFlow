import csv
from geopy.distance import great_circle

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--dms', required=True, help='path to csv')
parser.add_argument('--out', required=True, help='output folder')
parser.add_argument('--range', default=7000, help='cutoff range')


args = parser.parse_args()


Helsinki = (60.1699, 24.9384)

with open(args.dms, 'r') as infile, open(os.path.join(args.out, 'traffic.js'), 'w+') as jsfile:
    bins = []
    js_content = []

    raw_points = []

    i = 0

    for line in infile.readlines():
        # if i > 1000:
        #     break

        tokens = line.split('\t')
        points = tokens[1].split(',')[:-1]

        for point in points:
            tokens = point.split(';')

            # hour = tokens[2].split(' ')[1].split(':')[0]
            # print(line)
            # if len(hour) < 22:
            #     hour = int(hour)
            #     if hour != 6:
            #         print(hour)



            gps_coords = list(map(lambda x: float(x[1:-1]), tokens[:2]))

            in_Helsinki = great_circle(Helsinki, (gps_coords[0], gps_coords[1])).meters < 7000

            if not in_Helsinki:
                continue

            raw_points.append(gps_coords)


        i+=1

    raw_points.sort(key=lambda x:x[0])
    raw_points = raw_points[::10]

    prev_point = None

    for raw_point in raw_points:
        if prev_point is None:
            js_content.append('\t[{}]'.format(', '.join(list(map(str, raw_point)) + ['1.0'])))
            prev_point = raw_point
        else:
            delta_lat = abs(raw_point[0] - prev_point[0])
            delta_long = abs(raw_point[1] - prev_point[1])

            if delta_lat > 0 or delta_long > 0:
                js_content.append('\t[{}]'.format(', '.join(list(map(str, raw_point)) + ['1.0'])))

            prev_point = raw_point

    jsfile.write('traffic_locations = [\n{}\n]'.format(',\n'.join(js_content)))

        # print(line)

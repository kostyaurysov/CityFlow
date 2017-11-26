import csv
from geopy.distance import great_circle



Helsinki = (60.1699, 24.9384)

with open('bins_gps_all.csv', 'r') as csvfile, open('bins_filtered_with_gps.csv', 'w+') as outfile, open('bins.js', 'w+') as jsfile:
    reader = csv.reader(csvfile, delimiter=';')

    bins = []

    js_content = []

    for row in reader:



        bin_type = row[15]
        # Filter by priority type
        # if not bin_type in ['I', 'II', 'III']:
        #     # skip
        #     continue

        volume = row[7]

        # Filter by volume type
        # if volume not in ['HKR - roska-astia, 30 litraa', 'HKR - roska-astia, 60 litraa',
        #                     'HKR - roska-astia, 75 litraa', 'HKR - roska-astia, 140 litraa']:
        #     # skip
        #     continue

        # Get GPS position
        bin_gps = row[-1][1:-1].split(' ')
        # remove comma
        bin_gps[0] = bin_gps[0][:-1]

        # in_Helsinki = great_circle(Helsinki, (float(bin_gps[0]), float(bin_gps[1]))).meters < 10000

        # if not in_Helsinki:
        #     continue

        result = bin_gps
        result.append(bin_type)
        result.append(volume)

        outfile.write(';'.join(result))
        outfile.write('\n')

        js_content.append("\t[{}, {}, '{}', '{}', 1, 1]".format(*result))





        # bins.append((bin_gps[1:-1], volume, bin_type))
    jsfile.write('bin_locations = [\n{}\n]'.format(',\n'.join(js_content)))

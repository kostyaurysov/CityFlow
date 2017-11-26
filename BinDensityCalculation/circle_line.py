import math

import random
import numpy as np
import cv2
import csv
from csv import DictWriter

with open('bins.csv') as csvfile:
    rows = csv.reader(csvfile,delimiter =';')
    trash_bins = list(rows)

with open('people.dms') as ppl:
    content = ppl.readlines()
content = [x.replace('\'','').strip('\n') for x in content]

imies = dict()
for val in content:
    line_i = val.split('\t')
    str_i = line_i[1].split(',')
    final_i = [x.split(';') for x in str_i]
    imies[line_i[0]] = final_i

# R is in km
def distance_between_points(lat1,lon1,lat2,lon2):
    R = 6371e3
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


# print(imies['F4928F4E0E576DCA'])
imies_encoding = dict()
res_t = [0] * len(trash_bins)
with open("intersections.txt", "w+") as output:
    for i in imies.keys():
        lst = []
        for j in imies[i]:
            for idx, k in enumerate(trash_bins):
                d = distance_between_points(float(k[0]),float(k[1]),float(j[0]),float(j[1]))
                if(d<100):
                    lst.append(idx)
        imies_encoding[i] = set(lst)
        for jk in imies_encoding[i]:
            res_t[jk]+=1
        output.write(i+':'+' '.join(str(x) for x in lst)+'\n')

with open("results.txt", "w+") as output2:
    output2.write(' '.join(str(x) for x in res_t))

print(imies_encoding)





field_size = 512
radius = 60


def lineMagnitude (x1, y1, x2, y2):
    lineMagnitude = math.sqrt(math.pow((x2 - x1), 2)+ math.pow((y2 - y1), 2))
    return lineMagnitude

#Calc minimum distance from a point and a line segment (i.e. consecutive vertices in a polyline).
def DistancePointLine (x1, y1, x2, y2, px, py):
    #http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
    LineMag = lineMagnitude(x1, y1, x2, y2)

    if LineMag < 0.00000001:
        DistancePointLine = 9999
        return DistancePointLine

    u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
    u = u1 / (LineMag * LineMag)

    if (u < 0.00001) or (u > 1):
        #// closest point does not fall within the line segment, take the shorter distance
        #// to an endpoint
        # ix = lineMagnitude(px, py, x1, y1)
        # iy = lineMagnitude(px, py, x2, y2)
        # if ix > iy:
        #     DistancePointLine = iy
        # else:
        #     DistancePointLine = ix
        DistancePointLine = -1
    else:
        # Intersecting point is on the line, use the formula
        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        DistancePointLine = lineMagnitude(px, py, ix, iy)

    return DistancePointLine

# while(True):
#     img = np.zeros((field_size,field_size, 3), np.uint8)
#     ax_i = int(random.uniform(0, 1)*field_size)
#     ay_i = int(random.uniform(0, 1)*field_size)
#     bx_i = int(random.uniform(0, 1)*field_size)
#     by_i = int(random.uniform(0, 1)*field_size)
#     cx_i = int(random.uniform(0, 1)*field_size)
#     cy_i = int(random.uniform(0, 1)*field_size)
#     img = cv2.circle(img,(cx_i,cy_i), radius, (0,0,255), -1)
#     img = cv2.line(img, (ax_i, ay_i),(bx_i, by_i), (255, 0, 0), 2)
#
#     a_inside = (ax_i - cx_i) ** 2 + (ay_i - cy_i) ** 2 < radius ** 2
#     b_inside = (bx_i - cx_i) ** 2 + (by_i - cy_i) ** 2 < radius ** 2
#     if a_inside or b_inside:
#         ans = True
#     else:
#         dist = DistancePointLine(ax_i,ay_i,bx_i,by_i,cx_i,cy_i)
#         if(dist < 0 or dist > radius):
#             ans = False
#         else:
#             ans = True
#     cv2.putText(img, str(ans), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
#     cv2.imshow('newwin',img)
#     cv2.waitKey(0)


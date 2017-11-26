import math

import random
import numpy as np
import cv2
import csv
from csv import DictWriter


before_cntr1 = 0
before_cntr2 = 0
before_cntr3 = 0

after_cntr1 = 0
after_cntr2 = 0
after_cntr3 = 0
coeff = 0.52
with open("output.csv", "w") as f:
    with open('results.txt',) as res_txt:
        with open('bins.csv') as csvfile:
            rows = csv.reader(csvfile, delimiter =';')
            trash_bins = list(rows)
            lst = res_txt.readline()
            lst = lst.split()
            lst = [float(i) for i in lst]
            mn_i = np.mean(np.array(lst))
            std_i = np.std(np.array(lst))
            print('left')
            print(mn_i - std_i * coeff)
            print('right')
            print(mn_i + std_i * coeff)

            for ind, val in enumerate(trash_bins):
                if val[2] == 'I' or val[2] == 'KA1' or val[2] == 'KB1' or val[2] == 'H1':
                    before_cntr1+=1
                elif val[2]=='II' or val[2] == 'KA2' or val[2] == 'KB2' or val[2] == 'H2':
                    before_cntr2+=1
                else:
                    before_cntr3+=1

                if lst[ind] < mn_i-std_i*coeff:
                    val.append(1)
                    after_cntr1+=1
                elif lst[ind] > mn_i+std_i*coeff:
                    val.append(3)
                    after_cntr3+=1
                else:
                    val.append(2)
                    after_cntr2+=1
                val.append(lst[ind])
            writer = csv.writer(f)
            writer.writerows(trash_bins)

print('Before===================')
print("class1:"+str(before_cntr1))
print("class2:"+str(before_cntr2))
print("class3:"+str(before_cntr3))
print('After===================')
print("class1:"+str(after_cntr1))
print("class2:"+str(after_cntr2))
print("class3:"+str(after_cntr3))
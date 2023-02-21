import sys
import os
import csv
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

with open(r"C:\Users\nikit\notebooks\data\rba-dataset.csv", 'r') as f:
    i = 0
    data = []
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if i == 0:
            data.append([row[k].replace(" ", "_").replace("-", "_").replace("[", "").replace("]", "").lower()
                         for k in range(len(row))])
            i += 1
            continue
        data.append(row)
        i += 1
        if i == 100000:
            with open(r"C:\Users\nikit\notebooks\data\test.csv", 'w') as file:
                writer = csv.writer(file, delimiter=',', lineterminator='\n')
                writer.writerows(data)
                print("done")
            break

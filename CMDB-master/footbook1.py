import django
django.setup()
from assets.models import CarInfo
import re

with open('combine.csv', 'r', encoding='utf-8') as f:
    a = f.readline().split(',')
    num = 1
    while len(a) != 1:


        q = CarInfo(num, a[1], a[2], a[3], a[5],
                   a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[14], a[15], a[16], a[17], a[18])
        q.save()
        num += 1

        a = f.readline().split(',')

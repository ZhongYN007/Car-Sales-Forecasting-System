import django
django.setup()
from assets.models import Salesrank

with open('salesrank.csv', 'r', encoding='utf-8') as f:
    a = f.readline().split(',')
    while len(a) != 1:
        q = Salesrank(brand=a[2], type=a[0], price=a[1], sales=a[3][:-2])
        q.save()


        a = f.readline().split(',')

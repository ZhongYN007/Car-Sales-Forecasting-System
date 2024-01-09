import django
django.setup()
from assets.models import CarDetail

with open('chexinghebing.csv', 'r', encoding='utf-8') as f:
    a = f.readline().split(',')
    while len(a) != 1:
        a[0] = a[0].replace("/","-")
        q = CarDetail(update_date=a[0], brand=a[3], type=a[1], price=a[2], sales=a[4][:-2])
        q.save()


        a = f.readline().split(',')

import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "noonch_catch.settings")
django.setup()

from chat.models import *  # django.setup() ���Ŀ� ����Ʈ�ؾ� ������ ���� ����

CSV_PATH_PRODUCTS = 'noonchi.csv'
with open(CSV_PATH_PRODUCTS, encoding='UTF8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)  # ��½� �Բ� ��µǴ� ��ù���� �����ϰ� ����ϱ� ����
    for row in data_reader:
        content = Pic()
        content.answer = row[0]
        content.url = row[1]

        content.save()
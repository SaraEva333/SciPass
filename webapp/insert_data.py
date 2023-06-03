import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')

# Configure Django settings
django.setup()

from app.models import Sciedit, Iff, Quart, Specialty
import csv

def read_csv_file(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)

def insert_data():
    # Read the CSV files
    sciedit_data = read_csv_file('D:\Курсовая\sciedit.csv')
    iff_data = read_csv_file('D:\Курсовая\IF.csv')
    quart_data = read_csv_file('D:\Курсовая\quart.csv')
    specialty_data = read_csv_file('D:\Курсовая\specialty.csv')

    # Insert data into the Sciedit model
    for item in sciedit_data:
        Sciedit.objects.create(
            seid=item['seid'],
            issn=item['issn'],
            title=item['title']
        )

    # Insert data into the Iff model
    for item in iff_data:
        Iff.objects.create(
            ifid=item['ifid'],
            if_value=item['if_value'],
            db=item['db'],
            year=item['year'],
            seid_id=item['seid']
        )

    # Insert data into the Quart model
    for item in quart_data:
        Quart.objects.create(
            qid=item['qid'],
            current_quartile=item['current_quartile'],
            db=item['db'],
            year=item['year'],
            seid_id=item['seid']
        )

    # Insert data into the Specialty model
    for item in specialty_data:
        Specialty.objects.create(
            spid=item['spid'],
            code=item['code'],
            dat=item['dat'],
            seid_id=item['seid']
        )



import os
import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


def import_csv(path='customers.csv'):
    csv_rows = []

    # import csv
    print("Importing CSV.")
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            csv_rows.append(row)

    # remove the first row as it's just header information
    csv_rows.pop(0)
    return csv_rows


def bulk_customer_import(csv_file):
    csv_rows = import_csv(csv_file)

    missed_list = []
    for i, row in enumerate(csv_rows):
        email = row[0]

        if User.objects.filter(email=email).exists():
            print("Customer added: " + email)
            continue

        active = row[1]
        if active == "active":
            print("MISSED: " + email)
            missed_list.append(email)

    print('Finished. Skipped: [%s]' % ', '.join(map(str, missed_list)))


class Command(BaseCommand):
    help = 'Parses csv and checks whether that customer has been added to the system or not.'

    def add_arguments(self, parser):
        parser.add_argument(
             'csv_file',
             help='path to csv file',
             type=str,
        )

    def handle(self, *args, **options):
        print("Importing users...")

        csv_file = options.get('csv_file', '')
        if not os.path.isfile(csv_file):
            print('file not found!')
            return

        bulk_customer_import(csv_file)

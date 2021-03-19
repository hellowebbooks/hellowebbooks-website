import os
import csv

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.http import HttpRequest

from books import helpers
from books.models import Customer, Product, Membership


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


def add_customer(email, hello_web_app, hello_web_design, active):
    # create user
    user = User.objects.create_user(
        username=email.replace("@", "").replace(".", ""),
        email=email,
        password=User.objects.make_random_password(),
    )

    # create Customer from user
    customer = Customer.objects.create(user=user)

    # make appropriate Memberships based on form
    if hello_web_app:
        hwa_product_obj = Product.objects.get(name="Hello Web App")
        Membership.objects.create(
            customer=customer,
            product=hwa_product_obj,
            paperback=False,
            video=False,
        )

    if hello_web_design:
        hwd_product_obj = Product.objects.get(name="Hello Web Design")
        Membership.objects.create(
            customer=customer,
            product=hwd_product_obj,
            paperback=False,
            video=False,
        )

    # send User an email with how to access and reset the password
    request = HttpRequest()
    request.META['SERVER_NAME'] = 'hellowebbooks.com'
    request.META['SERVER_PORT'] = '443'
    request.session = {}
    helpers.send_giftee_password_reset(
        request,
        user.email,
        "Admin Add",
        'registration/admin_add_password_reset_subject.txt',
        'registration/admin_add_password_reset_email.txt',
    )

    # invite the person into the slack channel
    """
    if active == "active":
        print("Sending person to Slack: " + user.email)
        if not settings.DEBUG:
            product_name = "Hello Web Books"
            if hello_web_app and not hello_web_design:
                product_name = "Hello Web App"
            elif hello_web_design and not hello_web_app:
                product_name = "Hello Web Design"
            helpers.invite_to_slack(user.email, product_name)
    else:
        print("Skipping Slack: " + user.email)
    """

    return


def bulk_customer_import(csv_file):
    csv_rows = import_csv(csv_file)

    pass_list = []
    for i, row in enumerate(csv_rows):
        email = row[0]

        if User.objects.filter(email=email).exists():
            pass_list.append(email)
            print("Skipping, already added: " + email)
            continue

        hello_web_app = row[1]
        hello_web_design = row[2]
        active = row[3]

        if active == "bounced":
            pass_list.append(email)
            print("Skipping, bouncing email: " + email)
            continue

        add_customer(email, hello_web_app, hello_web_design, active)

    print('Finished. Skipped: [%s]' % ', '.join(map(str, pass_list)))


class Command(BaseCommand):
    help = 'Bulk imports customers into the HWA system.'

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

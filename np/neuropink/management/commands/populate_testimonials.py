import csv
import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from neuropink.models import Testimonials


def random_date(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


start_date = timezone.make_aware(timezone.datetime(2023, 1, 1))
end_date = timezone.now()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--fajl', type=str,
                            help='CSV Testimonials.', required=True)

    def handle(self, *args, **options):
        testimonials_file = options['fajl']

        with open(testimonials_file, mode='r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            header = next(reader)

            rows = list(reader)
            random.shuffle(rows)

            for row in rows:
                ime = row[0]
                prezime = row[1]
                review = row[2]

                Testimonials.objects.create(
                    first_name=ime,
                    last_name=prezime if random.random() < 0.65 else "",
                    review=review,
                    created_at=random_date(start_date, end_date),
                    approved=True,
                )
        print('done')

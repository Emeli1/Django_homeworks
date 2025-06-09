import csv
from decimal import Decimal
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone_data in phones:
            # Преобразуем данные
            name=phone_data['name']
            price=Decimal(phone_data['price'])
            image=phone_data['image']
            release_date=timezone.datetime.strptime(phone_data['release_date'], '%Y-%m-%d').date()
            lte_exists = phone_data['lte_exists'].lower() in ['true', '1', 't'] # Преобразование в Boolean
            slug=slugify(phone_data['name'])

            # Используем update_or_create
            obj, created = Phone.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'price': price,
                    'image': image,
                    'release_date': release_date,
                    'lte_exists': lte_exists,
                }
            )
            if created:
                print(f'Создана новая запись: {obj}')
            else:
                print(f'Обновлена существующая запись: {obj}')


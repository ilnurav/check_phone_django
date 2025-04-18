import os
import csv
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from phone_checker.models import PhoneRange

CSV_URLS = [
    'https://opendata.digital.gov.ru/downloads/ABC-3xx.csv',
    'https://opendata.digital.gov.ru/downloads/ABC-4xx.csv',
    'https://opendata.digital.gov.ru/downloads/ABC-8xx.csv',
    'https://opendata.digital.gov.ru/downloads/DEF-9xx.csv',
]


class Command(BaseCommand):
    help = 'Update phone number ranges from official sources'

    def handle(self, *args, **options):
        self.stdout.write("Starting update of phone number ranges...")

        # Создаем папку для кэша CSV, если ее нет
        csv_cache_dir = os.path.join(settings.BASE_DIR, 'data', 'csv_cache')
        os.makedirs(csv_cache_dir, exist_ok=True)

        # Очищаем старые данные
        PhoneRange.objects.all().delete()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        for url in CSV_URLS:
            filename = os.path.basename(url)
            local_path = os.path.join(csv_cache_dir, filename)

            try:
                # Пытаемся скачать файл
                self.stdout.write(f"Downloading {url}...")
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                # Сохраняем локальную копию
                with open(local_path, 'wb') as f:
                    f.write(response.content)

                content = response.content.decode('utf-8')
                self.process_csv(content, filename)

            except (requests.RequestException, IOError) as e:
                self.stdout.write(self.style.WARNING(f"Failed to download {url}: {str(e)}"))
                self.stdout.write("Trying to use local cache...")

                if os.path.exists(local_path):
                    try:
                        with open(local_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        self.process_csv(content, filename)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error processing local file {local_path}: {str(e)}"))
                else:
                    self.stdout.write(self.style.ERROR(f"No local cache available for {filename}"))

    def process_csv(self, content, filename):
        reader = csv.reader(content.splitlines(), delimiter=';')
        next(reader)  # Пропускаем заголовок

        batch = []
        processed = 0

        for row in reader:
            if len(row) >= 8:
                try:
                    batch.append(PhoneRange(
                        abc=row[0],
                        start=int(row[1]),
                        end=int(row[2]),
                        capacity=int(row[3]) if row[3] else 0,
                        operator=row[4],
                        region=row[5],
                        territory_gar=row[6],
                        inn=row[7]
                    ))

                    if len(batch) >= 1000:
                        PhoneRange.objects.bulk_create(batch)
                        processed += len(batch)
                        batch = []
                        self.stdout.write(f"{filename}: Processed {processed} records...")

                except (ValueError, IndexError) as e:
                    self.stdout.write(self.style.WARNING(f"Skipping malformed row: {str(e)}"))

        if batch:
            PhoneRange.objects.bulk_create(batch)
            processed += len(batch)

        self.stdout.write(self.style.SUCCESS(f"Successfully processed {filename}: {processed} records"))
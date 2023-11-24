import json
from django.core.management.base import BaseCommand
from users.models import WorldPopulation

class Command(BaseCommand):
    help = 'Load world population data from JSON file'

    def handle(self, *args, **options):
        with open('dataset_world_population_by_country_name.json') as f:
            data = json.load(f)

        for entry in data:
            WorldPopulation.objects.create(
                place=entry['place'],
                pop1980=entry['pop1980'],
                pop2000=entry['pop2000'],
                pop2010=entry['pop2010'],
                pop2022=entry['pop2022'],
                pop2023=entry['pop2023'],
                pop2030=entry['pop2030'],
                pop2050=entry['pop2050'],
                country=entry['country'],
                area=entry['area'],
                landAreaKm=entry['landAreaKm'],
                cca2=entry['cca2'],
                cca3=entry['cca3'],
                netChange=entry['netChange'],
                growthRate=entry['growthRate'],
                worldPercentage=entry['worldPercentage'],
                density=entry['density'],
                densityMi=entry['densityMi'],
                rank=entry['rank']
            )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))

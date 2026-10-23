from django.core.management.base import BaseCommand
from recommendations.models import RecommendationRule

class Command(BaseCommand):
    help = 'Seed default waste recommendation rules'

    def handle(self, *args, **options):
        rules = [
            {
                'category': 'organic',
                'bin_type': 'Green (Wet Waste Bin)',
                'bin_color_code': '#2E8B57',
                'biodegradable': True,
                'suggestion': 'Place the waste in the designated organic/wet-waste stream. Where appropriate, organic waste can be composted for soil enrichment.'
            },
            {
                'category': 'recyclable',
                'bin_type': 'Blue (Dry Recyclable Bin)',
                'bin_color_code': '#3B82F6',
                'biodegradable': False,
                'suggestion': 'Rinse or clean container residues if necessary. Place the item in the designated blue dry-recyclable waste stream for reprocessing.'
            },
            {
                'category': 'hazardous',
                'bin_type': 'Red / Yellow (Hazardous Waste Bin)',
                'bin_color_code': '#B45309',
                'biodegradable': False,
                'suggestion': 'Do NOT mix with ordinary municipal waste. Deposit at a designated hazardous waste drop-off point or specialized collection bin.'
            },
        ]

        for r in rules:
            obj, created = RecommendationRule.objects.update_or_create(
                category=r['category'],
                defaults=r
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{action} rule for {r["category"]}'))

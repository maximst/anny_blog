from django.core.management.base import BaseCommand

from blog.utils import instagram_parser


class Command(BaseCommand):
    help = 'Get posts from instagram'

    def handle(self, *args, **options):
        instagram_parser()

        self.stdout.write(self.style.SUCCESS('Successfully!'))

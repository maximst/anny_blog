import random
from django.conf import settings


def get_default_views_count(min_views=None, max_views=None):
    count = random.randint(
        min_views or settings.MIN_VIEWS_COUNT,
        max_views or settings.MAX_VIEWS_COUNT
    )
    return count

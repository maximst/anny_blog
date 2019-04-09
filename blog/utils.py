import re
import md5
import json
import random
import datetime
import requests
from django.conf import settings
from django.template.defaultfilters import slugify


def get_default_views_count(min_views=None, max_views=None):
    count = random.randint(
        min_views or settings.MIN_VIEWS_COUNT,
        max_views or settings.MAX_VIEWS_COUNT
    )
    return count


class InstagramAPI(object):
    api_url = 'https://www.instagram.com/graphql/query/'
    channel_url = 'https://www.instagram.com/{channel_name}/'
    re_json = re.compile('window\.\_sharedData\s*=\s*(?P<json>.+);</script>', re.I)
    _params = {
        'query_hash': settings.INSTAGRAM_QUERY_HASH,
    }
    pages = 12
    _rhx_gis = None
    _api = None
    _after = None
    _channel_id = None

    def __init__(self, channel_name):
        self._after = None
        self._api = requests.session()
        resp = requests.get(self.channel_url.format(channel_name=channel_name))
        result = self.re_json.search(resp.text)
        if result:
            data = json.loads(result.groupdict()['json'])
            self._channel_id = data['entry_data']['ProfilePage'][0]['graphql']['user']['id']
            self._rhx_gis = data['rhx_gis']

    def get_next_page(self):
        params = self._params.copy()
        variables = {
            'first': self.pages,
            'id': self._channel_id
        }
        if self._after:
            variables['after'] = self._after
        params['variables'] = json.dumps(variables, separators=(',', ':'))
        signature = md5.md5('{}:{}'.format(self._rhx_gis, json.dumps(variables, separators=(',', ':')))).hexdigest()
        result = self._api.get(self.api_url, params=params, headers={'x-instagram-gis': signature})
        if not result.ok:
            return ([], False)

        posts = result.json()['data']['user']['edge_owner_to_timeline_media']['edges']
        page_info = result.json()['data']['user']['edge_owner_to_timeline_media']['page_info']

        self._after = page_info['end_cursor']

        return (posts, page_info['has_next_page'])


def _instagram_create_channel_posts(category, channel):
    api = InstagramAPI(channel.channel)
    has_next = True

    while has_next:
        try:
            posts, has_next = api.get_next_page()
        except Exception:
            has_next = False
        else:
            [_create_blog(category, post['node']) for post in posts]


def _create_blog(category, post):
    from blog.models import InstagramBlog, InstagramImage

    all_text = [l['node']['text'] for l in post['edge_media_to_caption']['edges']]
    tags = filter(lambda s: s.startswith('#'), ' '.join(all_text).split())
    title = all_text and all_text[0].replace('#', '') or ''

    ib, created = InstagramBlog.objects.get_or_create(
        inst_id=post['id'],
        category=category,
        defaults={
            'short_code': post['shortcode'],
            'inst_user': post['owner']['username'],
            'title': title,
            'body': '\n<br />\n'.join(all_text),
            'create_time': datetime.datetime.fromtimestamp(post['taken_at_timestamp']),
            'tags': tags,
            'slug': slugify(title or str(post['id']))
        }
    )


def instagram_parser():
    from blog.models import InstagramChannel, InstagramCategory
    for category in InstagramCategory.objects.filter(enabled=True):
        for channel in category.channels.filter(enabled=True):
            _instagram_create_channel_posts(category, channel)

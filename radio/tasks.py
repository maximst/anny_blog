from django.conf import settings

import requests
from BeautifulSoup import BeautifulSoup


def vk_login():
    url = 'https://oauth.vk.com/authorize'
    query = {
        'client_id': settings.VK_STANDALONE_APP_ID,
        'scope': 'audio,groups,stats',
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'display': 'page',
        'v': '5.2',
        'response_type': 'token',
    }
    r = requests.get(url, params=query)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text)
        form = soup.find('form')
        action = dict(form.attrs)['action']
        inputs = form.findAll('input')

        post_data = {}
        for input in inputs:
            attrs = dict(input.attrs)
            if attrs['name'] != 'submit':
                post_data[attrs['name']] = attrs.get('value')

        post_data['email'] = ''
        post_data['pass'] = ''

        r = requests.post(action, data=post_data)
        return r

def get_audio():
    vk_login()

if __name__ == '__main__':
    get_audio()

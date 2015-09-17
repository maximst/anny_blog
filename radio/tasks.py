import requests
import urllib2
from BeautifulSoup import BeautifulSoup
import os
import sys
import vkontakte
import commands
from datetime import datetime

add_path = '/'.join(os.path.split(os.path.abspath(__file__))[0].split('/')[:-1])
sys.path.append(add_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anny_blog.settings")

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
from django.conf import settings
from django.core.files import File
from radio.models import Audio

SESSION = requests.Session()

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
    r = SESSION.get(url, params=query)

    if r.status_code == 200:
        r = post_login_data(r)
        for i in range(3):
            try:
                query = r.url.split('#')[1]
            except IndexError:
                soup = BeautifulSoup(r.text)
                form = soup.find('form')
                action = dict(form.attrs)['action']
                r = SESSION.post('%s%s' % ('/'.join(r.url.split('/')[:-1]), action), data={'code': settings.VK_PHONE})
#                r = post_login_data(r)
            else:
                break

        query = r.url.split('#')[-1]
        args = dict(item.split('=') for item in query.split('&'))

        return args['access_token']


def post_login_data(r):
    soup = BeautifulSoup(r.text)
    form = soup.find('form')
    action = dict(form.attrs)['action']
    inputs = form.findAll('input')

    post_data = {}
    for input in inputs:
        attrs = dict(input.attrs)
        if attrs['name'] != 'submit':
            post_data[attrs['name']] = attrs.get('value')

    post_data['email'] = settings.VK_EMAIL
    post_data['pass'] = settings.VK_PASS

    return SESSION.post(action, data=post_data)


def add_song(song):
    mp3_file = os.path.join(Audio.file_dir(), 'tmp', '%i.mp3' % song['aid'])

    fd_mp3 = open(mp3_file, 'w+')
    result = urllib2.urlopen(song['url'])
    fd_mp3.write(result.read())
    fd_mp3.close()
    result = None
    del result

    ogg_file = os.path.join(Audio.file_dir(), 'tmp',
                            '%s.ogg' % song['aid'].__str__())

    converted = False
    takes = 10
    take = 0

    while not converted and take < takes:
        command = 'ffmpeg -y -i %s -acodec libvorbis -ar 44100 -aq 2.3 %s' \
                                                % (mp3_file, ogg_file)
        print '[%s] INFO: Convert "%s"' % (datetime.utcnow(), command)
        result = commands.getoutput(command)

        fd_ogg = None
        fd_mp3 = None
        try:
            fd_ogg = open(ogg_file)
            fd_mp3 = open(mp3_file)
        except Exception as e:
            print '[%s] ERROR: Exception "%s"\n Command"%s\n%s"' % (datetime.utcnow(),
                                                                    e, command,
                                                                    result)
        else:
            converted = True

        take += 1

    song.pop('owner_id', None)
    song.pop('url', None)

    audio = Audio(**song)
    if fd_ogg:
        audio.ogg.save('%i.ogg' % song['aid'], File(fd_ogg))
    if fd_mp3:
        audio.mp3.save('%i.mp3' % song['aid'], File(fd_mp3))
    audio.save()

    fd_ogg.close()
    fd_mp3.close()

    os.remove(mp3_file)
    os.remove(ogg_file)


def get_audio():
    token = vk_login()
    vk = vkontakte.API(token=token)
    vk_audio = vk.audio.get(gid=settings.VK_GROUP_ID)
    vk_aids = []
    db_aids = Audio.objects.all().values_list('aid', flat=True)

    for audio in vk_audio:
        vk_aids.append(audio['aid'])

        if audio['aid'] not in db_aids:
            print '[%s] INFO: Create audio instance %s - %s ...' % (datetime.utcnow(),
                                                                audio['artist'],
                                                                audio['title'])
            add_song(audio)
            print '[%s] INFO: Done ...' % datetime.utcnow()

    # Delete removed vk songs
    Audio.objects.filter().exclude(aid__in=vk_aids).delete()


if __name__ == '__main__':
    get_audio()

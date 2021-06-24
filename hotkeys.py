import pyscreenshot as ImageGrab
from vk_messages import MessagesAPI
from vk_messages.utils import get_random
import vk
from vk.utils import LoggingSession, get_form_action, get_url_query
import keyboard
import json
import requests
from urllib import parse
import uuid

VERSION = '5.131'

def upload_photo(api, filename):
    upload = api.photos.getMessagesUploadServer(v=VERSION)
    upload_url = upload['upload_url']
    resp = requests.post(upload_url, files = {'file': open(filename, 'rb')}).json()
    response = api.photos.saveMessagesPhoto(server=resp['server'], photo=resp['photo'], hash=resp['hash'], latitude='0', longitude='0', caption='photo-' + str(uuid.uuid4()), v=VERSION)
    return response


def get_access_token(login, password, client_id='7884254', scope='offline,photos', redirect_uri='https://oauth.vk.com/blank.html'):
    
    auth_session = LoggingSession()
    login_url = 'https://m.vk.com'
    response = auth_session.get(login_url)
    login_form_action = get_form_action(response.text)
    if not login_form_action:
        raise ValueError('VK changed login flow')
    login_form_data = {
        'email': login,
        'pass': password,
    }
    response = auth_session.post(login_form_action, login_form_data)

    response_url_query = get_url_query(response.url)

    if 'remixsid' in auth_session.cookies or 'remixsid6' in auth_session.cookies:
        auth_url = f'https://oauth.vk.com/authorize'
        auth_data = {
            'client_id': client_id,
            'display': 'mobile',
            'response_type': 'token',
            'scope': scope,
            'v': '5.28',
        }
        response = auth_session.post(auth_url, auth_data)
        response_url = response.url
        parsed = parse.parse_qsl(response_url.replace('https://oauth.vk.com/auth_redirect?', '', 1))
        for p in parsed:
            if 'access_token' in p[1]:
                redirect = parse.unquote(p[1])
                data = parse.parse_qsl(redirect.replace(redirect_uri + '#', '', 1))
                for d in data:
                    if d[0] == 'access_token':
                        return d[1]
        raise ValueError('failed')

    if 'sid' in response_url_query:
        raise ValueError('Cpatcha')
    elif response_url_query.get('act') == 'authcheck' or 'security_check' in response_url_query:
        raise ValueError(response.text)
    else:
        message = 'Authorization error (incorrect password)'
        raise ValueError(message)

def send_screen(api: vk.API, messages, peer_id):
    try:
        im = ImageGrab.grab()
        im.save('screen.jpg')

        filename = 'screen.jpg'
        photos_list = upload_photo(api, filename)
        attachment = 'photo{owner_id}_{id}'.format(**photos_list[0])
        print(attachment)
        messages.method('messages.send', user_id=peer_id,
                        message='Скрин',
                        attachment=attachment,
                        random_id=get_random())
    except Exception as e:
        print(e)


def send_text(text, messages, peer_id):
    messages.method('messages.send', user_id=peer_id, message=text, random_id=get_random())


def get_text_sender(text, messages, peer_id):
    def sender():
        try:
            send_text(text, messages, peer_id)
        except Exception as e:
            print(e)
    return sender

if __name__ == '__main__':
    auth = json.loads(open('vk-auth.json', encoding='utf-8').read())
    login, password = auth['login'], auth['password']
    access_token = get_access_token(login, password)
    messages = MessagesAPI(login=login, password=str(password.encode('ANSI')).replace('\\x', '%')[2:-1],
                        cookies_save_path='sessions/')
    peer_id = auth['peer']
    session = vk.Session(access_token=access_token)
    api = vk.API(session)
    commands = json.loads(open('hotkeys.json', encoding='utf-8').read())
    commands.pop('Alt + S', None)
    commands.pop('Alt + Q', None)
    keyboard.add_hotkey('Alt + S', lambda: send_screen(api, messages, peer_id))
    for key in commands:
        keyboard.add_hotkey(key, get_text_sender(commands[key], messages, peer_id))
    keyboard.wait('Alt + Q')

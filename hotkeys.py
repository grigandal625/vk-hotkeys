import pyscreenshot as ImageGrab
from vk_messages import MessagesAPI
from vk_messages.utils import get_random
from vk_api import VkUpload
import vk_api
import keyboard
import json


def send_screen():
    im = ImageGrab.grab()
    im.save('screen.jpg')
    upload = VkUpload(vk_session)
    photos = ['screen.jpg']
    photo_list = upload.photo_wall(photos)
    attachment = 'photo{owner_id}_{id}'.format(**photo_list[0])
    print(attachment)
    messages.method('messages.send', user_id=peer_id,
                    message='Скрин',
                    attachment=attachment,
                    random_id=get_random())


def send_text(text):
    messages.method('messages.send', user_id=peer_id, message=text, random_id=get_random())


if __name__ == '__main__':
    auth = json.loads(open('vk-auth.json').read())
    login, password = auth['login'], auth['password']
    messages = MessagesAPI(login=login, password=str(password.encode('ANSI')).replace('\\x', '%')[2:-1],
                        cookies_save_path='sessions/')
    peer_id = auth['peer']
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    commands = json.loads(open('hotkeys.json').read())
    keyboard.add_hotkey('Alt + S', lambda: send_screen())
    for key in commands:
        keyboard.add_hotkey(key, lambda: send_text(commands[key]))
    keyboard.wait('Alt + Q')

import os, time, requests
from helium import *
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
url = os.environ['SITE_URL']
username = os.environ['LOGIN_USERNAME']
password = os.environ['LOGIN_PASSWORD']
chat_id = os.environ['CHAT_ID']
token = os.environ['BOT_TOKEN']
api_url = f"{os.environ['BOT_API_URL']}{token}/"
permitted_authors = ['user', 'CM', 'goldman', 'Theoracle', 'kaplun', 'CLT']


def get_id_list():
    id_list = ''
    with open('db.txt') as f:
        for line in f:
            id_list += line

    return id_list.split(';') if id_list else []


def update_id_list(id_list):
    with open('db.txt', 'a') as f:
        f.write(id_list)


def send_to_telegram(data):
    id_list = get_id_list()
    id_list_to_update = ''
    for mess in data:
        if id_list and mess['msg_id'] in id_list:
            continue
        elif 'https://docs.google.com/spreadsheets/d/1-QjZJNXgTVmSlXfs2aqZftN--DXJUC6kZizu0vHMlbo' in mess['href']:
            continue
        elif mess['href'].startswith('https://forum.zangertradingu.com'):
            continue
        elif mess["author"][:-1] not in permitted_authors:
            continue
        mess_link = mess["href"]
        mess_author = mess["author"]
        mess_time = mess["time"]
        text = f'<b>{mess_author}</b>\n{mess_time}\n<a href="{mess_link}">Ссылка на картинку</a>'
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        try:
            resp = requests.post(api_url + method, params)
        except Exception as e:
            print('error while sending mess to chat', e)
        id_list_to_update += f';{mess["msg_id"]}'
        update_id_list(id_list_to_update)
        # add id to csv
    # return resp


def run():
    all_links = find_all(S('.main-message-container .message-text a'))
    data_to_send = []
    for link in all_links:
        parent = link.web_element.find_element_by_xpath('..')
        grand_parent = parent.find_element_by_xpath('..')
        msg_id = grand_parent.find_element_by_xpath('..').get_attribute('id')
        msg_time = grand_parent.find_element_by_class_name('message-date').text.split(' ')[1]
        data = {
            'msg_id': msg_id,
            'author': grand_parent.find_element_by_class_name('message-user-name').text,
            'href': link.web_element.get_attribute('href'),
            'time': msg_time
        }
        data_to_send.append(data)

    send_to_telegram(data_to_send)


if __name__=='__main__':
    start_chrome(url, headless=True)
    click('Username')
    write(username, into=S('#rumbletalk-username'))
    write(password, into=S('#rumbletalk-password'))
    click('Log in')
    time.sleep(2)
    while True:
        run()
        time.sleep(60)
    kill_browser()
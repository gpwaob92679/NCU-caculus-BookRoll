from io import BytesIO
import re

from bs4 import BeautifulSoup
from PIL import Image
import requests

from utils import *


def save_images(session: requests.Session, save_path, url: str):
    pattern = re.compile('(?<=contents=)[0-9a-f]*')
    content_id = pattern.search(url).group(0)
    # print(content_id)

    page = 1
    while True:
        filename = f'out_{page}.jpg'
        img_url = f'https://bookroll.org.tw/contents/unzipped/{content_id}_1/OPS/images/{filename}'
        print(img_url)

        r_img = session.get(img_url)

        if r_img.text.startswith('<html'):  # Error message when page
            break

        img = Image.open(BytesIO(r_img.content))
        img.save(save_path / filename)

        page += 1


def main():
    download_path = get_path('./jpg')

    session = requests.Session()

    login_url = 'https://brpt.bookroll.org.tw/login/index.php'
    r_login = session.get(login_url)
    logintoken = BeautifulSoup(r_login.text, 'html.parser').find('input', {'name': 'logintoken'})['value']
    username = input('Enter username: ')
    password = input('Enter password: ')
    login_data = {'logintoken': logintoken, 'username': username, 'password': password}
    r_login = session.post(login_url, data=login_data)

    r_lti_redirect = session.get('https://brpt.bookroll.org.tw/mod/lti/launch.php?id=2911')
    r_lti_redirect_soup = BeautifulSoup(r_lti_redirect.text, 'html.parser')
    r_lti_redirect_inputs = r_lti_redirect_soup.find_all('input')
    r_lti_redirect_inputs_dict = dict()
    for tag in r_lti_redirect_inputs:
        r_lti_redirect_inputs_dict[tag['name']] = tag['value']
    # print(r_lti_redirect_inputs_dict)

    r_list = session.post(r_lti_redirect_soup.find('form')['action'], data=r_lti_redirect_inputs_dict)
    r_list_soup = BeautifulSoup(r_list.text, 'html.parser')
    r_list_a = r_list_soup.find_all('a', href=True)
    for tag in r_list_a:
        # print(tag)
        pattern = re.compile('第.*章')
        match = pattern.match(tag.text)
        if match:
            print(f'Saving "{tag.text}"...')
            save_path = get_path(download_path / tag.text)
            save_images(session, save_path, tag['href'])
            print('Done\n')


if __name__ == '__main__':
    main()

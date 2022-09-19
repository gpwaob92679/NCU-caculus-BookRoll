import argparse
from getpass import getpass
from io import BytesIO
from pathlib import Path
import re
from typing import Optional

from bs4 import BeautifulSoup
from PIL import Image
import requests

from utils import *


class BookRollDownloader:
    login_url = 'https://brpt.bookroll.org.tw/login/index.php'

    def __init__(self):
        self.session = requests.Session()

    def _download_image(self, save_file: Path, url: str) -> None:
        r_img = self.session.get(url)
        if r_img.text.startswith('<html'):  # Image not found
            raise FileNotFoundError

        img = Image.open(BytesIO(r_img.content))
        img.save(save_file)

    def _download_chapter(self, save_dir: Path, url: str) -> None:
        pattern = re.compile('(?<=contents=)[0-9a-f]*')
        content_id = pattern.search(url).group(0)

        page = 1
        while True:
            filename = f'out_{page}.jpg'
            img_url = (
                f'https://bookroll.org.tw/contents/unzipped/{content_id}_1/'
                f'OPS/images/{filename}')
            print(img_url)

            try:
                self._download_image(save_dir / filename, img_url)
            except FileNotFoundError:
                break

            page += 1

    def login(self,
              username: Optional[str] = None,
              password: Optional[str] = None) -> None:
        if username is None:
            print('BookRoll username not found in command-line arguments.')
            username = input('Please enter your BookRoll username: ')
        if password is None:
            print('BookRoll password not found in command-line arguments.')
            password = getpass('Please enter your BookRoll password: ')

        r_login = self.session.get(self.login_url)
        logintoken = BeautifulSoup(r_login.text, 'html.parser').find(
            'input', {'name': 'logintoken'})['value']
        login_data = {
            'logintoken': logintoken,
            'username': username,
            'password': password,
        }
        r_login = self.session.post(self.login_url, data=login_data)

    def download(self, download_path):
        r_lti_redirect = self.session.get(
            'https://brpt.bookroll.org.tw/mod/lti/launch.php?id=2911')
        r_lti_redirect_soup = BeautifulSoup(r_lti_redirect.text, 'html.parser')
        r_lti_redirect_inputs = r_lti_redirect_soup.find_all('input')
        r_lti_redirect_inputs_dict = dict()
        for tag in r_lti_redirect_inputs:
            r_lti_redirect_inputs_dict[tag['name']] = tag['value']
        # print(r_lti_redirect_inputs_dict)

        r_list = self.session.post(r_lti_redirect_soup.find('form')['action'],
                                   data=r_lti_redirect_inputs_dict)
        r_list_soup = BeautifulSoup(r_list.text, 'html.parser')
        r_list_a = r_list_soup.find_all('a', href=True)
        for tag in r_list_a:
            # print(tag)
            pattern = re.compile('第.*章')
            match = pattern.match(tag.text)
            if match:
                print(f'Saving "{tag.text}"...')
                save_path = get_path(download_path / tag.text)
                self._download_chapter(save_path, tag['href'])
                print('Done\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--download_path',
                        default='./jpg',
                        type=str,
                        help='Destination folder for downloaded files.')
    parser.add_argument('--username',
                        type=str,
                        help='Username to log in to BookRoll.')
    parser.add_argument('--password',
                        type=str,
                        help='Password to log in to BookRoll. Use this '
                        'argument with CAUTION though, as it is NOT '
                        'recommended to store passwords in plain text.')
    args = parser.parse_args()
    download_path = get_path(args.download_path)

    downloader = BookRollDownloader()
    downloader.login(args.username, args.password)
    downloader.download(download_path)


if __name__ == '__main__':
    main()

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
    rti_redirect_url = 'https://brpt.bookroll.org.tw/mod/lti/launch.php?id=2911'

    def __init__(self):
        self.session = requests.Session()

    def _send_form(
            self,
            url: str,
            form_attrs: Optional[dict[str, str]] = None,
            form_inputs: Optional[dict[str, str]] = None) -> requests.Response:
        request = self.session.get(url)
        request_soup = BeautifulSoup(request.text, 'html.parser')
        form = request_soup.find('form', form_attrs)

        if form_inputs is None:
            form_inputs = {}

        for tag in form.find_all('input'):
            if not tag['name'] in form_inputs:
                form_inputs[tag['name']] = tag['value']

        return self.session.post(form['action'], form_inputs)

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

        r_login = self._send_form(self.login_url, {'id': 'login'}, {
            'username': username,
            'password': password
        })

    def download(self, download_path):
        r_list = self._send_form(self.rti_redirect_url, {'id': 'ltiLaunchForm'})
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

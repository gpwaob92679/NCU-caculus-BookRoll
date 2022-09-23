import argparse
from getpass import getpass
from io import BytesIO
from pathlib import Path
import re
import time
from typing import Optional

from bs4 import BeautifulSoup
from deprecation import deprecated
from PIL import Image
import requests
from tqdm import tqdm

from utils import *


class BookRollDownloader:
    login_url = 'https://brpt.bookroll.org.tw/login/index.php'
    rti_redirect_url = 'https://brpt.bookroll.org.tw/mod/lti/launch.php?id=2911'

    def __init__(self):
        self.session = requests.Session()
        self.content_list_request = None
        self.content_list_soup = None
        self.content_list_a_tags = None

    def _send_form(
            self,
            url: str,
            form_attrs: Optional[dict[str, str]] = None,
            form_inputs: Optional[dict[str, str]] = None) -> requests.Response:
        form_request = self.session.get(url)
        form_request_soup = BeautifulSoup(form_request.text, 'html.parser')
        form_tag = form_request_soup.find('form', form_attrs)

        if form_inputs is None:
            form_inputs = {}

        for tag in form_tag.find_all('input'):
            if not tag['name'] in form_inputs:
                form_inputs[tag['name']] = tag['value']

        return self.session.post(form_tag['action'], form_inputs)

    def _get_content_list(self):
        self.content_list_request = self._send_form(self.rti_redirect_url,
                                                    {'id': 'ltiLaunchForm'})
        self.content_list_soup = BeautifulSoup(self.content_list_request.text,
                                               'html.parser')
        self.content_list_a_tags = self.content_list_soup.find_all('a',
                                                                   href=True)

    def _download_image(self, save_file: Path, url: str) -> None:
        img_request = self.session.get(url)
        if img_request.text.startswith('<html'):  # Image not found
            raise FileNotFoundError

        img = Image.open(BytesIO(img_request.content))
        img.save(save_file)

    @deprecated(details='Use _download_content_pdf instead to download '
                'higher-quality PDFs directly from the server.')
    def _download_content_images(self, save_dir: Path, content_id: str) -> None:
        page = 1
        while True:
            filename = f'out_{page}.jpg'
            img_url = (
                f'https://bookroll.org.tw/contents/unzipped/{content_id}_1/'
                f'OPS/images/{filename}')
            print(img_url)

            try:
                self._download_image(save_dir / filename, img_url)
            except FileNotFoundError:  # Reached the page after the last page
                break

            page += 1

    def _download_content_pdf(self, save_file: Path, content_id: str) -> None:
        header = self.content_list_soup.find('meta',
                                             {'id': '_csrf_header'})['content']
        token = self.content_list_soup.find('meta', {'id': '_csrf'})['content']
        csrf_header = {header: token}

        output_request = self.session.post(
            'https://bookroll.org.tw/book/pdfoutput/',
            {'viewerUrl': content_id},
            headers=csrf_header)
        output_response = [
            x for x in output_request.text[1:-1].replace('"', '').split(',')
        ]

        print('Waiting for server to process file', end='')
        while True:
            output_state_request = self.session.post(
                'https://bookroll.org.tw/book/pdfoutputstate/',
                {'tmpFile': output_response[1]},
                headers=csrf_header)
            if output_state_request.text == 'End':
                print('Done')
                break
            print('.', end='')
            time.sleep(2)

        output_data_request = self.session.post(
            'https://bookroll.org.tw/book/pdfoutputdata/',
            data={'tmpFile': output_response[1]},
            headers=csrf_header,
            stream=True)

        with tqdm.wrapattr(
                open(save_file, 'wb'),
                'write',
                desc=save_file.name,
                total=int(output_data_request.headers['content-length']),
                miniters=1,
        ) as f:
            for chunk in output_data_request.iter_content(1024):
                f.write(chunk)

    def login(self,
              username: Optional[str] = None,
              password: Optional[str] = None) -> None:
        if username is None:
            print('BookRoll username not found in command-line arguments.')
            username = input('Please enter your BookRoll username: ')
        if password is None:
            print('BookRoll password not found in command-line arguments.')
            password = getpass('Please enter your BookRoll password: ')

        login_request = self._send_form(self.login_url, {'id': 'login'}, {
            'username': username,
            'password': password
        })

        self._get_content_list()

    def download_slides(self, download_path: Path) -> None:
        pattern_chapter_name = re.compile('第.*章')
        pattern_content_id = re.compile('(?<=contents=)[0-9a-f]*')

        for tag in self.content_list_a_tags:
            # print(tag)
            match = pattern_chapter_name.match(tag.text)
            if match:
                content_id = pattern_content_id.search(tag['href']).group(0)
                filename = f'{tag.text}.pdf'
                print(f'Downloading "{filename}"...')
                self._download_content_pdf(download_path / filename, content_id)
                print(f'Successfully downloaded "{filename}".\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--download_path',
                        default='./pdf',
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
    downloader.download_slides(download_path)


if __name__ == '__main__':
    main()

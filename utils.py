from pathlib import Path

from bs4 import BeautifulSoup
import requests

def write_html_file(response: requests.Response, filename: str = None) -> None:
    if filename is None:
        filename = BeautifulSoup(response.text, 'html.parser').title.contents[0] + '.html'
    # print(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.text)

def get_path(p) -> Path:
    path = Path(p)
    if not path.exists():
        path.mkdir()
    return path

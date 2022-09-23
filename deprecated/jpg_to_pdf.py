import json
import re

import img2pdf
from pycnnum import cn2num

from utils import *


def folder_to_pdf(folder_path, pdf_path, pdf_filename):
    """Merge all .jpg files in folder to one .pdf file.

    The .jpg files are sorted by page number.
    """
    pattern = re.compile('\d+')
    jpg_list = []
    for file in folder_path.iterdir():
        if file.suffix == '.jpg':
            page_number = int(pattern.search(file.name).group(0))
            jpg_list.append((str(file), page_number))
    jpg_list.sort(key=lambda x: x[1])  # Sort by page number in filename
    jpg_list = [x[0] for x in jpg_list]

    with open(pdf_path / pdf_filename, 'wb') as f:
        f.write(img2pdf.convert(jpg_list))


def main():
    jpg_path = get_path('./jpg/')
    pdf_path = get_path('./pdf/')

    with open('chapters.json', 'r', encoding='utf-8') as f:
        chapter_num_to_name = json.load(f)

    for folder in jpg_path.iterdir():
        if folder.is_dir():
            pattern = re.compile('[一二三四五六七八九十]+')
            chapter_number_cn = pattern.search(folder.name).group(0)
            chapter_number_arabic = cn2num(chapter_number_cn)
            chapter_name = chapter_num_to_name[str(chapter_number_arabic)]
            pdf_filename = (f'Chapter {chapter_number_arabic} - '
                            f'{chapter_name}.pdf')

            folder_to_pdf(folder, pdf_path, pdf_filename)


if __name__ == '__main__':
    main()

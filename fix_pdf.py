from io import BytesIO
import json
from pathlib import Path
import re

import img2pdf
from pikepdf import Pdf
from pikepdf import PdfImage
from pycnnum import cn2num

from utils import *


def fix(src: Path, dest: Path) -> None:
    images = []  # Stored as bytes
    with Pdf.open(src) as pdf:
        for page in pdf.pages:
            lst = list(page.images.values())
            pdf_image = PdfImage(lst[0])

            bio = BytesIO()
            pdf_image.extract_to(stream=bio)
            bio.seek(0)

            images.append(bio)

    with open(dest, 'wb') as pdf_fixed:
        pdf_fixed.write(img2pdf.convert(images))


def main():
    pdf_path = get_path('./pdf/')

    with open('chapters.json', 'r', encoding='utf-8') as f:
        chapter_num_to_name = json.load(f)

    cn_number_pattern = re.compile('[一二三四五六七八九十]+')

    for f in pdf_path.iterdir():
        if f.suffix == '.pdf':
            chapter_number_cn = cn_number_pattern.search(f.name).group(0)
            chapter_number_arabic = cn2num(chapter_number_cn)
            chapter_name = chapter_num_to_name[str(chapter_number_arabic)]
            pdf_filename = (f'Chapter {chapter_number_arabic} - '
                            f'{chapter_name}.pdf')

            print(f'Fixing "{f.name}"...')
            fix(f, pdf_path / pdf_filename)
            print('Done\n')


if __name__ == '__main__':
    main()

import pytesseract
from PIL import Image

from pdf2image import convert_from_path
from pathlib import Path
import fitz
import re


pdfs_to_rename = list(Path('./').glob('*.pdf'))

# maybe add functionality to remove names?
for pdf in pdfs_to_rename:

    doc = fitz.open(pdf)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    outf = f'{pdf}_title_img.jpeg'
    pix.save(outf)

    text = pytesseract.image_to_string(Image.open(outf))[:70]

    text = text.replace(' ', '_').strip(' ')

    r = re.match(r'[a-zA-Z0-9_]+', text)
    if r:
        print(r.group(0).strip(' '))
        title = r.group(0).strip(' ')
        pdf.rename(f'{title}.pdf')

    # remove temp image generated
    Path(outf).unlink()

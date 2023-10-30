#!/usr/bin/python3
"""Generates qr image and saves into the qr image dir
File name:
    short_url+.png
Directory:
    qr_image
"""


import os
from PIL import Image, ImageDraw
import qrcode


def qr_gen(short_url=None):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
    )
    if len(short_url) > 1:
        qr.add_data(short_url)
        qr.make(fit=True)
    
        img = qr.make_image(fill_color="black", back_color="white")
        img_dir = 'app/static/images/qr_images'
        os.makedirs(img_dir, exist_ok=True)
        file_path = short_url.split('/')[3]
        file_name = os.path.join(img_dir, f'{file_path}.png')
        img.save(file_name)
        return f'{file_path}.png'
    else:
        pass


if __name__ == '__main__':
    qr_gen()

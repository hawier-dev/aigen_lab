import requests
from PySide6.QtGui import QImage, QPixmap
from huggingface_hub import HfApi


def convert_to_k_m(number):
    if number >= 1e6:
        return f"{number / 1e6:.2f}M"
    elif number >= 1e3:
        return f"{number / 1e3:.1f}K"
    else:
        return str(number)


def convert_size(size_bytes):
    size_unit = 1024
    kb = size_unit
    mb = size_unit**2
    gb = size_unit**3

    if size_bytes < kb:
        return f"{size_bytes} B"
    elif size_bytes < mb:
        return f"{size_bytes / kb:.2f} KB"
    elif size_bytes < gb:
        return f"{size_bytes / mb:.2f} MB"
    else:
        return f"{size_bytes / gb:.2f} GB"

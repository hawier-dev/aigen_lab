import requests
from PySide6.QtGui import QImage, QPixmap
from huggingface_hub import HfApi
import torch


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


def get_supported_format(branches):
    if torch.cuda.is_available():
        if torch.cuda.is_bf16_supported() and "bf16" in branches:
            return "bf16"
        elif "fp16" in branches:
            return "fp16"
        else:
            return "main"

    else:
        return "main"


def truncate_model_id(model_id):
    model_id = model_id.split("/")[1]
    return model_id


def get_available_devices():
    devices = []
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            device_name = torch.cuda.get_device_name(i)
            device_ref = f"cuda:{i}"
            devices.append((device_name, device_ref))
    devices.append(("CPU", "cpu"))
    return devices

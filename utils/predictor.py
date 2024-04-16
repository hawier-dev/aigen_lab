from datetime import datetime
from diffusers import StableDiffusionPipeline
import torch
import os
import json
from PySide6.QtCore import Signal, QObject

from utils.worker import PipelineLoaderThread


class Predictor(QObject):
    pipeline_loaded = Signal()

    def __init__(self, save_path):
        super().__init__()
        self.save_path = save_path
        self.pipe = None

    def load_pipeline(self, model_path, model_id, device):
        self.loader_thread = PipelineLoaderThread(model_path, model_id, device)
        self.loader_thread.finished.connect(self.on_pipeline_loaded)
        self.loader_thread.start()

    def on_pipeline_loaded(self, pipe):
        self.pipe = pipe
        self.pipeline_loaded.emit()

    def is_pipeline_loaded(self):
        return self.pipe is not None

    def generate_image(
        self,
        prompt,
        width=512,
        height=512,
        steps=60,
        guidance_scale=7.5,
        style="Normal",
        progress_callback=None,
    ):
        # Create a file name from the prompt
        folder_name = "".join(
            char for char in prompt.replace(" ", "_") if char.isalnum() or char == "_"
        )
        prompt_save_path = os.path.join(self.save_path, folder_name)

        index = 1
        while os.path.exists(prompt_save_path):
            prompt_save_path = os.path.join(self.save_path, f"{folder_name}_{index}")
            index += 1

        os.makedirs(prompt_save_path, exist_ok=True)

        file_name = f"{folder_name}.png"
        full_save_path = os.path.join(prompt_save_path, file_name)

        settings = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "guidance_scale": guidance_scale,
            "style": style,
            "date": datetime.now().strftime("%x %X"),
        }

        if style == "Artistic":
            prompt = f"Artistic {prompt}, in the style of impressionism"
        elif style == "Realistic":
            prompt = f"Realistic {prompt}, with high detail and photorealism"
        elif style == "Cartoon":
            prompt = f"Cartoon {prompt}, in a vibrant and stylized manner"
        elif style == "Minimalist":
            prompt = f"Minimalist {prompt}, with simple shapes and colors"
        else:
            prompt = f"{prompt}"

        results = self.pipe(
            prompt,
            width=int(width),
            height=int(height),
            num_inference_steps=int(steps),
            guidance_scale=float(guidance_scale),
            callback_on_step_end=progress_callback,
        )
        image = results.images[0]
        image.save(full_save_path)

        settings_path = os.path.join(prompt_save_path, "settings.json")
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=4)

        return full_save_path

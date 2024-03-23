import torch
from PySide6.QtCore import QRunnable, QObject, Signal, Slot, QThread
from diffusers import StableDiffusionPipeline


class WorkerSignals(QObject):
    finished = Signal(str)
    error = Signal(Exception)
    progress = Signal(int)


class ImageGenerationTask(QRunnable):
    def __init__(
        self,
        output_path,
        prompt,
        width,
        height,
        steps,
        guidance_scale,
        style,
        predictor,
    ):
        super().__init__()
        self.output_path = output_path
        self.prompt = prompt
        self.width = width
        self.height = height
        self.steps = steps
        self.guidance_scale = guidance_scale
        self.style = style
        self.predictor = predictor
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        def progress_callback(pipeline, step_index, timestep, callback_kwargs):
            progress = int((step_index / self.steps) * 100)
            self.signals.progress.emit(progress)

            return callback_kwargs

        try:
            image_path = self.predictor.generate_image(
                self.prompt,
                self.width,
                self.height,
                self.steps,
                self.guidance_scale,
                self.style,
                progress_callback=progress_callback,
            )
            self.signals.finished.emit(image_path)
        except Exception as e:
            self.signals.error.emit(e)


class PipelineLoaderThread(QThread):
    finished = Signal(object)

    def __init__(self, model_path, torch_dtype=torch.float16, device="cuda"):
        super().__init__()
        self.model_path = model_path
        self.torch_dtype = torch_dtype
        self.device = device

    def run(self):
        pipe = StableDiffusionPipeline.from_pretrained(
            self.model_path,
            torch_dtype=self.torch_dtype,
        ).to(self.device)
        self.finished.emit(pipe)

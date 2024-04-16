from PySide6.QtCore import QThread, Signal


class ModulesLoader(QThread):
    finished = Signal()
    progress = Signal(str)

    def run(self):
        self.progress.emit("Ładowanie torch...")
        import torch

        self.progress.emit("Ładowanie diffusers...")
        import diffusers

        self.finished.emit()

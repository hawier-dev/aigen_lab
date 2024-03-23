import os

import requests
from PySide6.QtCore import QThread, Signal
from huggingface_hub import list_repo_tree, hf_hub_url
from huggingface_hub.hf_api import RepoFile

from utils.functions import convert_size


class FileDownloader(QThread):
    progress_updated = Signal(str, str, str, float)
    download_complete = Signal(str)

    def __init__(self, repo_id, branch, output_path):
        super().__init__()
        self.repo_id = repo_id
        self.output_path = output_path
        self.branch = branch
        self.total_length = 0
        self.initial = 0

    def run(self):
        repo_tree = list_repo_tree(self.repo_id, recursive=True, revision=self.branch)
        self.get_total_size()
        for entry in repo_tree:
            if isinstance(entry, RepoFile):
                file_url = hf_hub_url(self.repo_id, filename=entry.path, revision=self.branch)
                local_path = os.path.join(self.output_path, entry.path)
                self.download_file(file_url, local_path)
        self.download_complete.emit(self.repo_id)

    def get_total_size(self):
        repo_tree = list_repo_tree(self.repo_id, recursive=True, revision=self.branch)
        for temp_entry in repo_tree:
            if isinstance(temp_entry, RepoFile):
                self.total_length += temp_entry.size

    def download_file(self, url, local_path):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        self.initial += len(chunk)
                        self.progress_updated.emit(
                            self.repo_id,
                            convert_size(self.initial),
                            convert_size(self.total_length),
                            self.initial / self.total_length * 100,
                        )

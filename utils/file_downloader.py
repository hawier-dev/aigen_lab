import os
import time
from requests.exceptions import ConnectionError, Timeout

import requests
from PySide6.QtCore import QThread, Signal
from huggingface_hub import list_repo_tree, hf_hub_url
from huggingface_hub.hf_api import RepoFile

from utils.functions import convert_size


class FileDownloader(QThread):
    progress_updated = Signal(str, str, str, float)
    download_complete = Signal(str)
    download_cancelled = Signal()

    def __init__(self, repo_id, branch, output_path):
        super().__init__()
        self.repo_id = repo_id
        self.output_path = output_path
        self.branch = branch
        self.total_length = 0
        self.current_size = 0
        self.cancel_flag = False

    def run(self):
        repo_tree = list_repo_tree(self.repo_id, recursive=True, revision=self.branch)
        self.get_total_size()
        for entry in repo_tree:
            if self.cancel_flag:
                self.download_cancelled.emit()
                break
            if isinstance(entry, RepoFile):
                file_url = hf_hub_url(
                    self.repo_id, filename=entry.path, revision=self.branch
                )
                local_path = os.path.join(self.output_path, entry.path)
                self.download_file(file_url, local_path)

        if not self.cancel_flag:
            self.download_complete.emit(self.repo_id)

    def cancel_download(self):
        self.cancel_flag = True

    def get_total_size(self):
        repo_tree = list_repo_tree(self.repo_id, recursive=True, revision=self.branch)
        for temp_entry in repo_tree:
            if isinstance(temp_entry, RepoFile):
                self.total_length += temp_entry.size

    def download_file(self, url, local_path, max_retries=5, delay=5):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        attempt = 0
        last_emit_time = time.time()

        while attempt < max_retries:
            try:
                with requests.head(url) as r:
                    r.raise_for_status()
                    web_file_size = int(r.headers.get("content-length", 0))

                if os.path.exists(local_path):
                    local_file_size = os.path.getsize(local_path)
                    print(
                        f"Local file size: {local_file_size}, Web file size: {web_file_size}"
                    )
                    if web_file_size == local_file_size:
                        self.current_size += local_file_size
                        self.progress_updated.emit(
                            self.repo_id,
                            convert_size(self.current_size),
                            convert_size(self.total_length),
                            self.current_size / self.total_length * 100,
                        )
                        return

                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(local_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if self.cancel_flag:
                                return
                            if chunk:
                                f.write(chunk)
                                self.current_size += len(chunk)
                                current_time = time.time()
                                if current_time - last_emit_time >= 1:
                                    self.progress_updated.emit(
                                        self.repo_id,
                                        convert_size(self.current_size),
                                        convert_size(self.total_length),
                                        self.current_size / self.total_length * 100,
                                    )
                                    last_emit_time = current_time
                break

            except ConnectionError:
                attempt += 1
                print(
                    f"Unable to connect to the internet. Attempt {attempt} of {max_retries}."
                )
                time.sleep(delay)
            except Timeout:
                print("The server response time has exceeded the timeout limit.")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

        if attempt == max_retries:
            print("Failed to download the file after the maximum number of attempts.")

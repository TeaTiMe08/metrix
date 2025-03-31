import os
import shutil


class FileUtils:
    """Class for file utilities."""
    @staticmethod
    def read_token_from_file(file_path=".github_token"):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return None

    @staticmethod
    def cleanup_frames_folder(temp_frames_dir):
        if os.path.exists(temp_frames_dir):
            shutil.rmtree(temp_frames_dir)
        os.makedirs(temp_frames_dir)

    @staticmethod
    def read_token_from_file(file_path=".github_token"):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return None

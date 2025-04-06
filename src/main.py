
import os

from config import Config
from file_utils import FileUtils
from frame_builder import FrameBuilder
from gif_builder import GifBuilder
from log_config import logger
from text_builder import TextBuilder

if __name__ == "__main__":
    try:
        logger.info(f"----------------------------------------------------")
        logger.info(f"[INITIALIZATION] - Fetching and preparing data")
        FileUtils.cleanup_frames_folder(Config.TEMP_FRAMES_DIR)
        text_lines = TextBuilder.generate_text()
        frame_rate = Config.FPS  # Maximum rate is 50 FPS, higher values make it slower
        activity_graphic = TextBuilder.generate_activity_graphic()
        FrameBuilder.create_typing_frames(text_lines, activity_graphic, Config.TEXT_COLOR, Config.BACKGROUND_COLOR, Config.TEMP_FRAMES_DIR)
        logger.info(f"----------------------------------------------------")
        logger.info(f"[BUILD] - Building GIF")
        file_path = os.path.abspath(f"{Config.OUTPUT_FILE_PATH}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        GifBuilder.generate_gif_ffmpeg(frame_rate, file_path, Config.TEMP_FRAMES_DIR)
        logger.info(f"----------------------------------------------------")
        logger.info(f"[END]")
        logger.info(f"GIF saved as {file_path}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

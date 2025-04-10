
import os
import time

from color_utils import ColorUtils
from config import Config
from file_utils import FileUtils
from frame_builder import FrameBuilder
from gif_builder import GifBuilder
from log_config import logger
from text_builder import TextBuilder

if __name__ == "__main__":
    try:
        text_color = os.getenv("TEXT_COLOR").lower()
        background_color = os.getenv("BACKGROUND_COLOR").lower()
        # Allow parallel executions
        frames_dir = Config.TEMP_FRAMES_DIR + "_" + str(int(time.time()))

        while True:
            # Restore original values on each iteration
            Config.BACKGROUND_COLOR, Config.TEXT_COLOR, Config.METHOD, Config.CONTRAST, _ = ColorUtils.resolve_colors(background_color, text_color, Config.MINIMUM_CONTRAST)
            file_path = os.path.abspath(f"output/random_combinations/{Config.BACKGROUND_COLOR}_{Config.TEXT_COLOR}.gif")

            # Check if the file already exists
            if os.path.exists(file_path):
                logger.info(f"File {file_path} already exists. Skipping this combination.")
                continue

            logger.info(f"----------------------------------------------------")
            logger.info(f"[INITIALIZATION] - Fetching and preparing data")

            # Cleanup frames folder
            FileUtils.cleanup_frames_folder(frames_dir)

            # Generate text and build frames
            text_lines = TextBuilder.generate_text()
            frame_rate = Config.FPS  # Maximum rate is 50 FPS, higher values make it slower
            activity_graphic = "         ▁ ▁▁ ▁▄▁__▁   _▄█▄_▄◘"
            logger.info(f"----------------------------------------------------")
            logger.info(f"[BUILD] - Building GIF")

            FrameBuilder.create_typing_frames(text_lines, activity_graphic, Config.TEXT_COLOR, Config.BACKGROUND_COLOR, frames_dir)

            # Save GIF file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            GifBuilder.generate_gif_ffmpeg(frame_rate, file_path, frames_dir)

            logger.info(f"----------------------------------------------------")
            logger.info(f"[END]")
            logger.info(f"GIF saved as {file_path}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

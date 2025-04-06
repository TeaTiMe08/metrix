import json
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from config import Config
from file_utils import FileUtils
from frame_builder import FrameBuilder
from gif_builder import GifBuilder
from log_config import logger
from text_builder import TextBuilder


def load_color_combinations(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def process_combination(queue, thread_id):
    try:
        while True:
            combination = queue.get()  # Blocks until an item is available
            if combination is None:  # Exit condition for when there are no tasks
                queue.task_done()  # Mark the task as done before breaking
                break

            # Load color combination
            background_color = combination["color1"]
            text_color = combination["color2"]

            file_path = os.path.abspath(f"src/tests/bulk/{background_color}_{text_color}.gif")

            # Check if the file already exists
            if os.path.exists(file_path):
                logger.info(f"[THREAD-{thread_id}] - File {file_path} already exists. Skipping this combination.")
                queue.task_done()  # Mark the task as done without processing
                continue

            # Create a unique folder for each thread
            frames_dir = f"frames_{thread_id}"
            os.makedirs(frames_dir, exist_ok=True)

            logger.info(f"----------------------------------------------------")
            logger.info(f"[THREAD-{thread_id}][INITIALIZATION] - Fetching and preparing data for: {background_color}, {text_color}")

            # Cleanup frames folder
            FileUtils.cleanup_frames_folder(frames_dir)

            # Generate text and build frames
            text_lines = TextBuilder.generate_text()
            frame_rate = Config.FPS  # Maximum rate is 50 FPS, higher values make it slower
            activity_graphic = "         ▁ ▁▁ ▁▄▁__▁   _▄█▄_▄◘"
            logger.info(f"----------------------------------------------------")
            logger.info(f"[THREAD-{thread_id}][BUILD] - Building GIF")

            FrameBuilder.create_typing_frames(text_lines, activity_graphic, text_color, background_color, frames_dir)

            # Save GIF file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            GifBuilder.generate_gif_ffmpeg(frame_rate, file_path, frames_dir)

            logger.info(f"----------------------------------------------------")
            logger.info(f"[THREAD-{thread_id}][END]")
            logger.info(f"GIF saved as {file_path}")

            queue.task_done()  # Mark the task as done after processing

    except Exception as e:
        logger.error(f"[THREAD-{thread_id}] An error occurred: {e}")
        raise

    finally:
        # Cleanup thread-specific folder after processing
        if os.path.exists(frames_dir):
            shutil.rmtree(frames_dir)
            logger.info(f"[THREAD-{thread_id}] - Temporary folder {frames_dir} deleted.")


if __name__ == "__main__":
    try:
        # Load the color combinations from the JSON file
        color_combinations = load_color_combinations("src/tests/color_combinations.json")

        # Define the number of threads to use (adjust as necessary)
        num_threads = 4

        # Create a queue and populate it with all combinations
        queue = Queue()
        for combination in color_combinations:
            queue.put(combination)

        # Create a ThreadPoolExecutor with a limited number of threads
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit the threads to start processing combinations
            futures = [
                executor.submit(process_combination, queue, thread_id)
                for thread_id in range(1, num_threads + 1)
            ]

            # Wait for all tasks in the queue to be processed
            queue.join()  # This will block until all tasks are processed

            # Insert None values into the queue to signal threads to stop
            for _ in range(num_threads):
                queue.put(None)  # Signal the threads to stop after completing work

            # Wait for all threads to complete
            for future in futures:
                future.result()

    except Exception as e:
        logger.error(f"An error occurred in main execution: {e}")
        raise

import os

import ffmpeg

from config import Config
from log_config import logger


class GifBuilder:
    """Class to generate GIF using ffmpeg."""

    @staticmethod
    def generate_gif_ffmpeg(frame_rate, output_file):
        # Ensure the frame directory exists and contains frames
        frames_dir = Config.TEMP_FRAMES_DIR
        if not os.path.exists(frames_dir):
            raise FileNotFoundError(f"The directory {frames_dir} does not exist.")

        frame_pattern = f"{frames_dir}/frame_%04d.png"
        if not any(os.path.isfile(os.path.join(frames_dir, f)) for f in os.listdir(frames_dir) if f.endswith(".png")):
            raise FileNotFoundError(f"No PNG frames found in {frames_dir}.")

        # Generate a palette to reduce gif size
        palette_file = f"{frames_dir}/palette.png"
        try:
            (
                ffmpeg.input(frame_pattern, r=frame_rate)
                .output(palette_file, vf="palettegen", r=frame_rate)
                .run(overwrite_output=True)
            )
        except ffmpeg.Error as e:
            logger.error(f"Error during palette generation: {e}")
            raise

        # Use the generated palette to create the optimized GIF
        try:
            (
                ffmpeg.filter(
                    [
                        ffmpeg.input(frame_pattern, r=frame_rate),
                        ffmpeg.input(palette_file),
                    ],
                    filter_name="paletteuse",
                    dither="heckbert",
                    new="False",
                )
                .output(output_file, loop=Config.LOOP)
                .run(overwrite_output=True)
            )
        except ffmpeg.Error as e:
            logger.error(f"Error during GIF creation: {e}")
            raise

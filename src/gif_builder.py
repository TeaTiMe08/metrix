import ffmpeg

from config import Config


class GifBuilder:
    """Class to generate GIF using ffmpeg."""
    @staticmethod
    def generate_gif_ffmpeg(frame_rate, output_file):
        # Generate a palette to reduce gif size
        palette_file = f"{Config.TEMP_FRAMES_DIR}/palette.png"
        (
            ffmpeg.input(f"{Config.TEMP_FRAMES_DIR}/frame_%04d.png", r=frame_rate)
            .output(palette_file, vf="palettegen", r=frame_rate)
            .run(overwrite_output=True)
        )

        # Use the generated palette to create the optimized GIF
        (
            ffmpeg.filter(
                [
                    ffmpeg.input(f"{Config.TEMP_FRAMES_DIR}/frame_%04d.png", r=frame_rate),
                    ffmpeg.input(palette_file),
                ],
                filter_name="paletteuse",
                dither="heckbert",
                new="False",
            )
            .output(output_file)
            .run(overwrite_output=True)
        )

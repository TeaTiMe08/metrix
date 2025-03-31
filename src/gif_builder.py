import ffmpeg

from config import Config


class GifBuilder:
    """Class to generate GIF using ffmpeg."""
    @staticmethod
    def generate_gif_ffmpeg(frame_rate, output_file):
        (
            ffmpeg.input(f"{Config.TEMP_FRAMES_DIR}/frame_%04d.png", r=frame_rate)
            .output(output_file, vf="scale=iw:ih:flags=neighbor", pix_fmt="pal8", loop=-1, r=frame_rate)
            .run(overwrite_output=True)
        )

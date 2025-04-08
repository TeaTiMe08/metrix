import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw, ImageFont

from config import Config
from file_utils import FileUtils
from glitch import Glitch


class FrameBuilder:
    """Class to create frames for the GIF."""
    @staticmethod
    def apply_glitch(typed_text, frame_count, glitches, glitch_probability, max_glitches):
        if random.random() < glitch_probability and len(glitches) < max_glitches:
            glitch_pos = random.randint(0, len(typed_text) - 1)
            if not any(glitch.position == glitch_pos for glitch in glitches) and typed_text[glitch_pos] != '\n':
                original_char = typed_text[glitch_pos]
                typed_text = typed_text[:glitch_pos] + random.choice(Config.GLITCH_SYMBOLS) + typed_text[glitch_pos + 1:]
                restore_frame = frame_count + random.randint(2, 10)
                glitches.append(Glitch(glitch_pos, original_char, restore_frame))
        return typed_text

    @staticmethod
    def restore_glitches(typed_text, frame_count, glitches, force_restore=False):
        for glitch in glitches[:]:
            if force_restore or frame_count >= glitch.restore_frame:
                typed_text = typed_text[:glitch.position] + glitch.original_char + typed_text[glitch.position + 1:]
                glitches.remove(glitch)
        return typed_text

    @staticmethod
    def create_frames(count, text, activity_graphic, text_color, background_color, text_font, symbol_font, frame_count, frames_dir):
        # Generate the frame
        img = Image.new("RGB", (Config.WIDTH, Config.HEIGHT), background_color)
        draw = ImageDraw.Draw(img)

        # Draw text
        draw.text((10, 10), text, font=text_font, fill=text_color)
        draw.text((10, Config.HEIGHT - 60), Config.ACTIVITY_TEXT, font=symbol_font, fill=text_color)
        draw.text((10, Config.HEIGHT - 32), activity_graphic, font=symbol_font, fill=text_color)

        # Draw frame box around activity graphic
        activity_length = len(activity_graphic)
        draw.text((10, Config.HEIGHT - 32), "‾" * activity_length, font=symbol_font, fill=text_color)
        draw.text((2, Config.HEIGHT - 33), "│" + " " * (activity_length - 1) + "│", font=symbol_font, fill=text_color)
        draw.text((2, Config.HEIGHT - 30), "│" + " " * (activity_length - 1) + "│", font=symbol_font, fill=text_color)
        draw.text((10, Config.HEIGHT - 11), "‾" * activity_length, font=symbol_font, fill=text_color)

        # Save the first frame
        frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
        img.save(frame_path)
        frame_count += 1

        # Copy the same frame for the remaining count-1 times
        for _ in range(count - 1):
            new_frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
            shutil.copy(frame_path, new_frame_path)
            frame_count += 1

        return frame_count

    @staticmethod
    def create_typing_frames(text_lines, activity_graphic, text_color, background_color, frames_dir):
        font = ImageFont.truetype(FileUtils.resolve_font_path(Config.FONT_PATH), Config.FONT_SIZE)
        symbol_font = ImageFont.truetype(FileUtils.resolve_font_path(Config.SYMBOL_FONT_PATH), Config.FONT_SIZE)

        typed_text = ""
        frame_count = 0
        max_glitches = Config.MAX_GLITCHES
        glitches = []
        glitch_probability = Config.GLITCH_PROBABILITY

        if isinstance(text_lines, str):
            text = text_lines
        else:
            try:
                text = "\n".join(text_lines)
            except TypeError:
                # If it's not iterable, convert to string as fallback
                text = str(text_lines)

        for idx, char in enumerate(text):
            typed_text += char

            if Config.GLITCHES:
                typed_text = FrameBuilder.apply_glitch(typed_text, frame_count, glitches, glitch_probability, max_glitches)
                typed_text = FrameBuilder.restore_glitches(typed_text, frame_count, glitches)

            frame_count = FrameBuilder.create_frames(1, typed_text + Config.TYPING_CHARACTER, activity_graphic, text_color, background_color, font, symbol_font, frame_count, frames_dir)

        for _ in range(6):
            if Config.GLITCHES:
                typed_text = FrameBuilder.restore_glitches(typed_text, frame_count, glitches)
            frame_count = FrameBuilder.create_frames(20, typed_text + Config.TYPING_CHARACTER, activity_graphic, text_color, background_color, font, symbol_font, frame_count, frames_dir)
            frame_count = FrameBuilder.create_frames(20, typed_text, activity_graphic, text_color, background_color, font, symbol_font, frame_count, frames_dir)

        # Final restoration of glitches
        if Config.GLITCHES and glitches:
            typed_text = FrameBuilder.restore_glitches(typed_text, frame_count, glitches, force_restore=True)
            frame_count = FrameBuilder.create_frames(1, typed_text + Config.TYPING_CHARACTER, activity_graphic, text_color, background_color, font, symbol_font, frame_count, frames_dir)

        return frame_count

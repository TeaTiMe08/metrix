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
        width, height = Config.WIDTH, Config.HEIGHT
        left_margin = 10

        # Create base image and draw context
        img = Image.new("RGB", (width, height), background_color)
        draw = ImageDraw.Draw(img)

        # Draw main text
        draw.text((left_margin, 10), text, font=text_font, fill=text_color)

        if Config.ACTIVITY:
            symbol_font_size = symbol_font.size
            padding = max(3, int(symbol_font_size * 0.25))
            box_border_width = max(1, int(symbol_font_size * 0.2))

            # Calculate positions
            activity_x = left_margin - 1 + padding
            activity_y = height - int(symbol_font_size * 1.7)
            activity_text_y = height - int(symbol_font_size * 3.2)

            # Get text dimensions for the activity graphic
            bbox = symbol_font.getbbox(activity_graphic)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_y_offset = bbox[1]

            # Calculate box properties
            box_top = activity_y - padding
            box_width = text_width + (padding * 2)
            box_height = text_height + (padding * 2)

            # Draw activity elements
            draw.text((left_margin, activity_text_y), Config.ACTIVITY_TEXT, font=symbol_font, fill=text_color)
            draw.rectangle([
                (activity_x - padding - 1, box_top - 1),
                (activity_x - padding + box_width, box_top + box_height)
            ], outline=text_color, width=box_border_width)
            draw.text((activity_x, box_top + padding - text_y_offset), activity_graphic, font=symbol_font, fill=text_color)

        # Save first frame
        frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
        img.save(frame_path)
        frame_count += 1

        # Duplicate for remaining frames
        for _ in range(count - 1):
            new_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
            shutil.copy(frame_path, new_path)
            frame_count += 1

        return frame_count

    @staticmethod
    def create_typing_frames(text_lines, activity_graphic, text_color, background_color, frames_dir):
        font = ImageFont.truetype(FileUtils.resolve_font_path(Config.FONT_PATH), Config.FONT_SIZE)
        symbol_font = ImageFont.truetype(FileUtils.resolve_font_path(Config.SYMBOL_FONT_PATH), Config.SYMBOL_FONT_SIZE)

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

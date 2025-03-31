import os
import random

from PIL import Image, ImageDraw, ImageFont

from config import Config
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
    def restore_glitches(typed_text, frame_count, glitches):
        for glitch in glitches[:]:
            if frame_count >= glitch.restore_frame:
                typed_text = typed_text[:glitch.position] + glitch.original_char + typed_text[glitch.position + 1:]
                glitches.remove(glitch)
        return typed_text

    @staticmethod
    def create_frames(count, text, activity_graphic, text_font, symbol_font, frame_count):
        for _ in range(count):
            img = Image.new("RGB", (Config.WIDTH, Config.HEIGHT), Config.BACKGROUND_COLOR)
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), text, font=text_font, fill=Config.TEXT_COLOR)
            draw.text((10, Config.HEIGHT - 60), Config.ACTIVITY_TEXT, font=symbol_font, fill=Config.TEXT_COLOR)
            draw.text((10, Config.HEIGHT - 32), activity_graphic, font=symbol_font, fill=Config.TEXT_COLOR)

            activity_length = len(activity_graphic)
            draw.text((10, Config.HEIGHT - 32), "‾" * (activity_length), font=symbol_font, fill=Config.TEXT_COLOR)
            draw.text((2, Config.HEIGHT - 33), "│" + " " * (activity_length - 1) + "│", font=symbol_font, fill=Config.TEXT_COLOR)
            draw.text((2, Config.HEIGHT - 30), "│" + " " * (activity_length - 1) + "│", font=symbol_font, fill=Config.TEXT_COLOR)
            draw.text((10, Config.HEIGHT - 11), "‾" * (activity_length), font=symbol_font, fill=Config.TEXT_COLOR)

            img.save(os.path.join(Config.TEMP_FRAMES_DIR, f"frame_{frame_count:04d}.png"))
            frame_count += 1
        return frame_count

    @staticmethod
    def create_typing_frames(text_lines, activity_graphic):
        font = ImageFont.truetype(Config.FONT_PATH, 20)
        symbol_font = ImageFont.truetype(Config.SYMBOL_FONT_PATH, 20)
        typed_text = ""
        frame_count = 0
        max_glitches = 4
        glitches = []
        glitch_probability = 0.03  # 3% chance of glitch in each frame

        text = "\n".join(text_lines)

        for idx, char in enumerate(text):
            typed_text += char

            if Config.GLITCHES:
                typed_text = FrameBuilder.apply_glitch(typed_text, frame_count, glitches, glitch_probability, max_glitches)
                typed_text = FrameBuilder.restore_glitches(typed_text, frame_count, glitches)

            frame_count = FrameBuilder.create_frames(1, typed_text + "█", activity_graphic, font, symbol_font, frame_count)

        for _ in range(6):
            if Config.GLITCHES:
                typed_text = FrameBuilder.restore_glitches(typed_text, frame_count, glitches)
            frame_count = FrameBuilder.create_frames(20, typed_text + "█", activity_graphic, font, symbol_font, frame_count)
            frame_count = FrameBuilder.create_frames(20, typed_text, activity_graphic, font, symbol_font, frame_count)

        return frame_count

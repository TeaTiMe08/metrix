import colorsys
import random

import matplotlib.colors as mcolors

from log_config import logger


class ColorUtils:
    NAMED_COLORS = list(mcolors.CSS4_COLORS)
    COLOR_MAP = mcolors.CSS4_COLORS
    VALID_METHODS = ["complementary", "contrasting", "shade"]

    @staticmethod
    def log_color_selection(text_color, background_color, text_method="", bg_method="", text_brightness=None, bg_brightness=None):
        """Logs the text and background color information with methods and brightness details."""
        bg_info = f" ({bg_method}{'-'+bg_brightness if bg_method == 'random' and bg_brightness else ''})" if bg_method else ""
        text_info = f" ({text_method}{'-'+text_brightness if text_method == 'random' and text_brightness else ''})" if text_method else ""

        logger.info(f"Background color{bg_info}: {background_color}")
        logger.info(f"Text color{text_info}: {text_color}")

    @staticmethod
    def resolve_colors(background_color, text_color, minimum_contrast):
        method = ""
        text_brightness = None
        bg_brightness = None
        modulation = None

        # Check for random-light or random-dark in text_color
        if text_color in ["random-light", "random-dark"]:
            text_brightness = text_color.split("-")[1]
            text_color = "random"

        # Check for random-light or random-dark in background_color
        if background_color in ["random-light", "random-dark"]:
            bg_brightness = background_color.split("-")[1]
            background_color = "random"

        # Handle different combinations of text_color and background_color
        is_text_random = text_color == "random"
        is_bg_random = background_color == "random"
        is_text_method = text_color in ColorUtils.VALID_METHODS
        is_bg_method = background_color in ColorUtils.VALID_METHODS

        # Both text and background are random
        if is_text_random and is_bg_random:
            # Get independent random colors for both text and background
            text_color = ColorUtils.get_random_color(text_brightness)
            background_color = ColorUtils.get_random_color(bg_brightness)
            ColorUtils.log_color_selection(text_color, background_color, "random", "random", text_brightness, bg_brightness)

        # Both text and background are valid methods
        elif is_text_method and is_bg_method:
            logger.warning("Both text and background colors are methods. Using random color for text.")
            text_color = ColorUtils.get_random_color(text_brightness)
            method = background_color
            background_color = ColorUtils.get_color(text_color, method)
            ColorUtils.log_color_selection(text_color, background_color, "random", method, text_brightness, bg_brightness)

        # One is random, one is a method
        elif is_text_random and is_bg_method:
            text_color = ColorUtils.get_random_color(text_brightness)
            method = background_color
            background_color = ColorUtils.get_color(text_color, method)
            ColorUtils.log_color_selection(text_color, background_color, "random", method, text_brightness, bg_brightness)
        elif is_bg_random and is_text_method:
            background_color = ColorUtils.get_random_color(bg_brightness)
            method = text_color
            text_color = ColorUtils.get_color(background_color, method)
            ColorUtils.log_color_selection(text_color, background_color, method, "random", text_brightness, bg_brightness)

        # Only text or background is random
        elif is_text_random:
            text_color = ColorUtils.get_random_color(text_brightness)
            method = random.choice(ColorUtils.VALID_METHODS)
            ColorUtils.log_color_selection(text_color, background_color, "random", "", text_brightness, bg_brightness)
        elif is_bg_random:
            background_color = ColorUtils.get_random_color(bg_brightness)
            method = random.choice(ColorUtils.VALID_METHODS)
            ColorUtils.log_color_selection(text_color, background_color, "", "random", text_brightness, bg_brightness)

        # Only text or background is a method
        elif is_text_method:
            method = text_color
            text_color = ColorUtils.get_color(background_color, method)
            ColorUtils.log_color_selection(text_color, background_color, method, "", text_brightness, bg_brightness)
        elif is_bg_method:
            method = background_color
            background_color = ColorUtils.get_color(text_color, method)
            ColorUtils.log_color_selection(text_color, background_color, "", method, text_brightness, bg_brightness)

        # No special processing needed
        else:
            ColorUtils.log_color_selection(text_color, background_color)

        # Check and adjust contrast if needed
        contrast = round(ColorUtils.contrast_ratio(text_color, background_color), 2)
        contrast_text = f"[{contrast}]"

        if contrast < minimum_contrast:
            logger.warning(f"Contrast ratio ({contrast}) is below ({minimum_contrast}). Adjusting colors...")
            iteration_count = 0
            max_iterations = 10

            # Determine which color to adjust based on which is a function or random
            color_to_adjust = "text"

            # If one color is random and the other is fixed, adjust the random one
            if is_text_random and not is_bg_random and not is_bg_method:
                color_to_adjust = "text"
            elif is_bg_random and not is_text_random and not is_text_method:
                color_to_adjust = "background"
            # If one is a method and one is fixed, adjust the method one
            elif is_bg_method and not is_text_method:
                color_to_adjust = "background"
            elif is_text_method and not is_bg_method:
                color_to_adjust = "text"
            # If neither is a function or random, randomly choose one
            elif not is_bg_method and not is_text_method and not is_bg_random and not is_text_random:
                color_to_adjust = random.choice(["text", "background"])

            original_color = text_color if color_to_adjust == "text" else background_color

            while contrast < minimum_contrast and iteration_count < max_iterations:
                if color_to_adjust == "text":
                    text_color = ColorUtils.get_random_shade_of_color(text_color)
                else:
                    background_color = ColorUtils.get_random_shade_of_color(background_color)

                contrast = round(ColorUtils.contrast_ratio(text_color, background_color), 2)
                iteration_count += 1

            if iteration_count == max_iterations:
                logger.error("ERROR: Max iterations reached, contrast may still be too low.")
                contrast_text = f"[{contrast}](MOD_ERROR)"
                modulation = "ERROR"
            else:
                adjusted_color = text_color if color_to_adjust == "text" else background_color
                logger.info(f"{color_to_adjust.title()} color ({original_color} modulated): {adjusted_color}")
                contrast_text = f"[{contrast}]"
                modulation = f"{original_color}->{adjusted_color}"

        return background_color, text_color, method, contrast_text, modulation

    @staticmethod
    def get_color(base_color, method):
        if method == "complementary":
            return ColorUtils.generate_complementary_color(base_color)
        elif method == "contrasting":
            return ColorUtils.get_contrasting_color(base_color)
        elif method == "shade":
            return ColorUtils.get_random_shade_of_color(base_color)
        return base_color  # Default fallback

    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert hex color code to RGB tuple (0-1 range)."""
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        # Convert to RGB
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b)

    @staticmethod
    def contrast_ratio(c1, c2):
        """Calculate the contrast ratio between two colors (using luminance)."""

        # Ensure the colors are in RGB format (matplotlib returns [0, 1] scale)
        if isinstance(c1, str):
            if c1.startswith('#'):
                c1 = ColorUtils.hex_to_rgb(c1)
            elif c1 in mcolors.CSS4_COLORS:
                c1 = mcolors.to_rgb(c1)
        if isinstance(c2, str):
            if c2.startswith('#'):
                c2 = ColorUtils.hex_to_rgb(c2)
            elif c2 in mcolors.CSS4_COLORS:
                c2 = mcolors.to_rgb(c2)

        def luminance(c):
            """Calculate the luminance of a color."""
            r, g, b = c
            # Apply the luminance formula using the sRGB values
            a = [r, g, b]
            for i in range(3):
                if a[i] <= 0.03928:
                    a[i] = a[i] / 12.92
                else:
                    a[i] = ((a[i] + 0.055) / 1.055) ** 2.4
            return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]

        # Calculate luminance for both colors
        lum1, lum2 = luminance(c1), luminance(c2)

        # Ensure the contrast ratio is calculated properly
        if lum1 > lum2:
            ratio = (lum1 + 0.05) / (lum2 + 0.05)
        else:
            ratio = (lum2 + 0.05) / (lum1 + 0.05)

        return ratio

    @staticmethod
    def closest_color_name(r, g, b):
        """Finds the closest named color to the given RGB values."""
        return min(ColorUtils.COLOR_MAP, key=lambda color: ColorUtils.color_distance((r, g, b), mcolors.to_rgb(ColorUtils.COLOR_MAP[color])))

    @staticmethod
    def color_distance(c1, c2):
        """Calculates the Euclidean distance between two RGB colors."""
        return sum((x - y) ** 2 for x, y in zip(c1, c2)) ** 0.5

    @staticmethod
    def get_random_color(brightness=None):
        """
        Returns a random, readable color name.

        Args:
            brightness (str, optional): 'light' for bright colors, 'dark' for dark colors, None for any color.
        """
        if brightness == "light":
            return ColorUtils.generate_random_light_color()
        elif brightness == "dark":
            return ColorUtils.generate_random_dark_color()
        return random.choice(ColorUtils.NAMED_COLORS)

    @staticmethod
    def generate_random_light_color():
        """Generates a random bright color (high brightness)."""
        h = random.random()  # Random hue
        s = random.uniform(0.4, 0.9)  # Mix of saturated and pastel colors
        v = random.uniform(0.7, 0.95)  # Consistently high brightness

        # Convert to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        # Boost one random channel slightly to add variety
        boost_channel = random.randint(0, 2)
        boost_amount = random.uniform(0.05, 0.15)

        if boost_channel == 0:
            r = min(1.0, r + boost_amount)
        elif boost_channel == 1:
            g = min(1.0, g + boost_amount)
        else:
            b = min(1.0, b + boost_amount)

        closest_color = ColorUtils.closest_color_name(r, g, b)
        return closest_color

    @staticmethod
    def generate_random_dark_color():
        """Generates a random dark color (low brightness)."""
        h = random.random()  # Random hue
        s = random.uniform(0.6, 1.0)  # Higher saturation for richer dark colors
        v = random.uniform(0.2, 0.45)  # Controlled brightness range to avoid black

        # Convert to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        # Boost one random channel slightly to avoid pure black/gray
        boost_channel = random.randint(0, 2)
        boost_amount = random.uniform(0.05, 0.15)

        if boost_channel == 0:
            r = min(1.0, r + boost_amount)
        elif boost_channel == 1:
            g = min(1.0, g + boost_amount)
        else:
            b = min(1.0, b + boost_amount)

        closest_color = ColorUtils.closest_color_name(r, g, b)
        return closest_color

    @staticmethod
    def is_gray(r, g, b, threshold=0.1):
        """Check if a color is gray (low saturation and high value)."""
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return s < threshold  # If saturation is below threshold, consider it gray

    @staticmethod
    def generate_complementary_color(color_name):
        """Generates a complementary color by ensuring harmony between brightness and saturation."""
        try:
            # Convert named color to RGB
            r, g, b = mcolors.to_rgb(mcolors.CSS4_COLORS[color_name])
        except KeyError:
            # If the color is invalid, default to white
            return "white"

        # Check if the color is gray or close to gray
        if ColorUtils.is_gray(r, g, b):
            # If gray, return a highly saturated color to provide contrast
            return ColorUtils.generate_random_light_color()

        # Convert to HSV
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # Adjust hue to find a complementary color
        comp_hue = (h + 0.5) % 1.0

        # Keep the same saturation and brightness, but adjust the hue to generate a new color
        comp_r, comp_g, comp_b = colorsys.hsv_to_rgb(comp_hue, s, v)

        # If the resulting color is too dark, adjust brightness
        if v < 0.3:
            comp_r, comp_g, comp_b = colorsys.hsv_to_rgb(comp_hue, min(1.0, s + 0.2), min(1.0, v + 0.3))

        # Return the complementary color as the closest color name
        return ColorUtils.closest_color_name(comp_r, comp_g, comp_b)

    @staticmethod
    def get_contrasting_color(color_name):
        """Finds a contrasting color for a given named color."""
        try:
            # Convert named color to RGB
            r, g, b = mcolors.to_rgb(mcolors.CSS4_COLORS[color_name])
        except KeyError:
            # If the color is invalid, default to white
            return "white"

        # Check if the color is gray or close to gray
        if ColorUtils.is_gray(r, g, b):
            # If gray, return a highly saturated color to provide contrast
            return ColorUtils.generate_random_light_color()

        # Convert to HSV
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # Adjust for very dark or very bright colors
        if v < 0.1:  # Too dark → generate a bright color
            return ColorUtils.generate_random_light_color()
        if v > 0.9:  # Too bright → generate a dull color
            return ColorUtils.generate_random_dark_color()

        # Compute complementary hue
        h = (h + 0.5) % 1.0  # Complementary color
        comp_r, comp_g, comp_b = colorsys.hsv_to_rgb(h, s, v)

        # Return the contrasting color as the closest color name
        return ColorUtils.closest_color_name(comp_r, comp_g, comp_b)

    @staticmethod
    def get_random_shade_of_color(base_color):
        """Generates a random shade of the given color name (lighter or darker)."""
        try:
            # Convert named color to RGB
            r, g, b = mcolors.to_rgb(mcolors.CSS4_COLORS[base_color])
        except KeyError:
            # If the color is invalid, default to white
            return "white"

        # Calculate the lightness of the color
        lightness = (r + g + b) / 3

        # Check if the color is too close to white or black
        if lightness > 0.9:
            # If the color is too close to white or black, randomize it
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            darken_factor = random.uniform(0.1, 0.5)
            r = max(0, r - darken_factor)
            g = max(0, g - darken_factor)
            b = max(0, b - darken_factor)
        elif lightness < 0.1:
            # If the color is too close to white or black, randomize it
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            lighten_factor = random.uniform(0.1, 0.5)
            r = min(1, r + lighten_factor)
            g = min(1, g + lighten_factor)
            b = min(1, b + lighten_factor)
        elif ColorUtils.is_gray(r, g, b):
            # If gray, generate a random color far from gray
            if random.choice([True, False]):
                return ColorUtils.generate_random_light_color()
            else:
                return ColorUtils.generate_random_dark_color()
        else:
            # Randomly decide whether to darken or lighten the color
            darken_factor = random.uniform(0.2, 0.5)
            lighten_factor = random.uniform(0.6, 1)

            # Randomly choose whether to darken or lighten the color
            if random.choice([True, False]):
                # Darken the color by reducing RGB values
                r = max(0, r - darken_factor)
                g = max(0, g - darken_factor)
                b = max(0, b - darken_factor)
            else:
                # Lighten the color by increasing RGB values
                r = min(1, r + lighten_factor)
                g = min(1, g + lighten_factor)
                b = min(1, b + lighten_factor)

        # Return the modified color as the closest color name
        return ColorUtils.closest_color_name(r, g, b)

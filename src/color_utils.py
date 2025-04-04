import colorsys
import random

import matplotlib.colors as mcolors

from log_config import logger


class ColorUtils:
    NAMED_COLORS = list(mcolors.CSS4_COLORS)
    COLOR_MAP = mcolors.CSS4_COLORS
    VALID_METHODS = ["complementary", "contrasting", "shade"]

    @staticmethod
    def resolve_colors(text_color, background_color, minimum_contrast):
        method = ""
        if text_color == background_color == "random":
            method = random.choice(ColorUtils.VALID_METHODS)
            if random.choice([True, False]):
                text_color = ColorUtils.get_random_color()
                background_color = ColorUtils.get_color(text_color, method)
                logger.info(f"Text color (random): {text_color}")
                logger.info(f"Background color ({method}): {background_color}")
            else:
                background_color = ColorUtils.get_random_color()
                text_color = ColorUtils.get_color(background_color, method)
                logger.info(f"Text color ({method}): {text_color}")
                logger.info(f"Background color (random): {background_color}")
        elif text_color in ColorUtils.VALID_METHODS and background_color in ColorUtils.VALID_METHODS:
            text_color = ColorUtils.get_random_color()
            method = background_color
            background_color = ColorUtils.get_color(text_color, method)
            logger.info(f"Text color (random): {text_color}")
            logger.info(f"Background color ({text_color}): {background_color}")
        elif text_color == "random" and background_color in ColorUtils.VALID_METHODS:
            text_color = ColorUtils.get_random_color()
            method = background_color
            background_color = ColorUtils.get_color(text_color, method)
            logger.info(f"Text color (random): {text_color}")
            logger.info(f"Background color ({method}): {background_color}")
        elif background_color == "random" and text_color in ColorUtils.VALID_METHODS:
            background_color = ColorUtils.get_random_color()
            method = text_color
            text_color = ColorUtils.get_color(background_color, method)
            logger.info(f"Text color ({method}): {text_color}")
            logger.info(f"Background color (random): {background_color}")
        elif text_color == "random":
            method = random.choice(ColorUtils.VALID_METHODS)
            text_color = ColorUtils.get_color(background_color, method)
            logger.info(f"Text color ({method}): {text_color}")
            logger.info(f"Background color: {background_color}")
        elif background_color == "random":
            method = random.choice(ColorUtils.VALID_METHODS)
            background_color = ColorUtils.get_color(text_color, method)
            logger.info(f"Text color: {text_color}")
            logger.info(f"Background color ({method}): {background_color}")
        elif text_color in ColorUtils.VALID_METHODS:
            method = text_color
            text_color = ColorUtils.get_color(background_color, method)
            logger.info(f"Text color ({method}): {text_color}")
            logger.info(f"Background color: {background_color}")
        elif background_color in ColorUtils.VALID_METHODS:
            method = background_color
            background_color = ColorUtils.get_color(text_color, method)
            logger.info(f"Text color: {text_color}")
            logger.info(f"Background color ({method}): {background_color}")
        else:
            logger.info(f"Text color: {text_color}")
            logger.info(f"Background color: {background_color}")

        contrast = round(ColorUtils.contrast_ratio(text_color, background_color), 2)
        contrast_text = f"[{contrast}]"

        if contrast < minimum_contrast:
            logger.warning(f"Contrast ratio ({contrast}) is below ({minimum_contrast}). Adjusting text color...")
            iteration_count = 0
            max_iterations = 10
            original_text_color = text_color

            while contrast < minimum_contrast and iteration_count < max_iterations:
                text_color = ColorUtils.get_random_shade_of_color(text_color)
                contrast = round(ColorUtils.contrast_ratio(text_color, background_color), 2)
                iteration_count += 1

            if iteration_count == max_iterations:
                logger.error("ERROR: Max iterations reached, contrast may still be too low.")
                contrast_text = f"[{contrast}](MOD_ERROR)"
            else:
                logger.info(f"Text color (modulated): {text_color}")
                contrast_text = f"[{contrast}](MOD_{original_text_color})"

        return text_color, background_color, method, contrast_text

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
    def contrast_ratio(c1, c2):
        """Calculate the contrast ratio between two colors (using luminance)."""

        # Ensure the colors are in RGB format (matplotlib returns [0, 1] scale)
        if c1 in mcolors.CSS4_COLORS:
            c1 = mcolors.to_rgb(c1)
        if c2 in mcolors.CSS4_COLORS:
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
    def get_random_color():
        """Returns a random, readable color name."""
        return random.choice(ColorUtils.NAMED_COLORS)

    @staticmethod
    def generate_random_bright_color():
        """Generates a random bright color (high saturation & brightness)."""
        h = random.random()  # Random hue
        s = random.uniform(0.7, 1.0)  # High saturation
        v = random.uniform(0.8, 1.0)  # High brightness
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        closest_color = ColorUtils.closest_color_name(r, g, b)
        return closest_color

    @staticmethod
    def generate_random_dull_color():
        """Generates a random dull color (low saturation & brightness)."""
        h = random.random()  # Random hue
        s = random.uniform(0.0, 0.8)  # Low saturation
        v = random.uniform(0.1, 0.4)  # Low brightness
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
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
            return ColorUtils.generate_random_bright_color()

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
            return ColorUtils.generate_random_bright_color()

        # Convert to HSV
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # Adjust for very dark or very bright colors
        if v < 0.1:  # Too dark → generate a bright color
            return ColorUtils.generate_random_bright_color()
        if v > 0.9:  # Too bright → generate a dull color
            return ColorUtils.generate_random_dull_color()

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
                return ColorUtils.generate_random_bright_color()
            else:
                return ColorUtils.generate_random_dull_color()
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

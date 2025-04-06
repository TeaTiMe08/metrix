import colorsys
import matplotlib.colors as mcolors


class ColorUtilsExtended:

    @staticmethod
    def is_shade(color1, color2):
        """Determine if two colors are shades of each other (same hue, diff lightness)."""
        rgb1 = mcolors.to_rgb(color1)
        rgb2 = mcolors.to_rgb(color2)

        h1, l1, s1 = colorsys.rgb_to_hls(*rgb1)
        h2, l2, s2 = colorsys.rgb_to_hls(*rgb2)

        hue_threshold = 0.1
        lightness_threshold = 0.3

        return abs(h1 - h2) < hue_threshold and abs(l1 - l2) > lightness_threshold

    @staticmethod
    def is_analogous(color1, color2):
        """Colors within ~30º on hue circle."""
        h1 = colorsys.rgb_to_hls(*mcolors.to_rgb(color1))[0]
        h2 = colorsys.rgb_to_hls(*mcolors.to_rgb(color2))[0]

        hue_diff = abs(h1 - h2)
        hue_diff = min(hue_diff, 1 - hue_diff)  # Wrap around

        return hue_diff < (30 / 360)

    @staticmethod
    def is_triadic(color1, color2):
        """Colors ~120º apart on hue circle."""
        h1 = colorsys.rgb_to_hls(*mcolors.to_rgb(color1))[0]
        h2 = colorsys.rgb_to_hls(*mcolors.to_rgb(color2))[0]

        hue_diff = abs(h1 - h2)
        hue_diff = min(hue_diff, 1 - hue_diff)

        return abs(hue_diff - (120 / 360)) < (15 / 360)

    @staticmethod
    def is_neutral(color1, color2):
        """Both colors are grayscale-like."""
        def is_grayish(rgb):
            r, g, b = rgb
            return abs(r - g) < 0.05 and abs(g - b) < 0.05

        return is_grayish(mcolors.to_rgb(color1)) and is_grayish(mcolors.to_rgb(color2))

    @staticmethod
    def is_warm_cold_pair(color1, color2):
        """One warm color, one cold color."""
        def hue_type(color):
            h = colorsys.rgb_to_hls(*mcolors.to_rgb(color))[0]
            return 'warm' if 0 <= h < (1 / 3) or h > (5 / 6) else 'cold'

        return hue_type(color1) != hue_type(color2)

    @staticmethod
    def is_same_family(color1, color2):
        """Both colors belong to the same general family (red, blue, green, etc.)."""
        def get_family(color):
            h = colorsys.rgb_to_hls(*mcolors.to_rgb(color))[0]
            if 0 <= h < (1 / 6):
                return 'red'
            elif (1 / 6) <= h < (2 / 6):
                return 'orange'
            elif (2 / 6) <= h < (3 / 6):
                return 'yellow'
            elif (3 / 6) <= h < (4 / 6):
                return 'green'
            elif (4 / 6) <= h < (5 / 6):
                return 'blue'
            else:
                return 'purple'

        return get_family(color1) == get_family(color2)

    @staticmethod
    def is_warm_pair(color1, color2):
        """Both colors are warm-toned."""
        def is_warm(color):
            h = colorsys.rgb_to_hls(*mcolors.to_rgb(color))[0]
            return 0 <= h < (1 / 3) or h > (5 / 6)

        return is_warm(color1) and is_warm(color2)

    @staticmethod
    def is_cold_pair(color1, color2):
        """Both colors are cold-toned."""
        def is_cold(color):
            h = colorsys.rgb_to_hls(*mcolors.to_rgb(color))[0]
            return (1 / 3) <= h < (5 / 6)

        return is_cold(color1) and is_cold(color2)

    @staticmethod
    def is_pastel_pair(color1, color2):
        """Both colors are pastel-like (low saturation, high lightness)."""
        def is_pastel(color):
            rgb = mcolors.to_rgb(color)
            h, l, s = colorsys.rgb_to_hls(*rgb)
            return s < 0.3 and l > 0.7

        return is_pastel(color1) and is_pastel(color2)

    @staticmethod
    def is_vivid_pair(color1, color2):
        """Both colors are vivid (high saturation)."""
        def is_vivid(color):
            rgb = mcolors.to_rgb(color)
            h, l, s = colorsys.rgb_to_hls(*rgb)
            return s > 0.7

        return is_vivid(color1) and is_vivid(color2)

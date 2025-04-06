import json
import os

from matplotlib import colors as mcolors

from color_utils import ColorUtils
from log_config import logger
from tests.color_utils_extended import ColorUtilsExtended

OUTPUT_FILE = "./src/tests/color_combinations.json"

def detect_combination_types(color1, color2, contrast):
    types = []

    # Contrast type if contrast is high
    if contrast >= 7:
        types.append("contrasting")

    # Complementary check
    complementary_of_1 = ColorUtils.get_color(color1, "complementary")
    if complementary_of_1 == color2:
        types.append("complementary")

    # Shade check (same hue, different lightness)
    if ColorUtilsExtended.is_shade(color1, color2):
        types.append("shade")

    # Analogous check
    if ColorUtilsExtended.is_analogous(color1, color2):
        types.append("analogous")

    # Triadic check
    if ColorUtilsExtended.is_triadic(color1, color2):
        types.append("triadic")

    # Neutral check
    if ColorUtilsExtended.is_neutral(color1, color2):
        types.append("neutral")

    # Warm/cold pair check
    if ColorUtilsExtended.is_warm_cold_pair(color1, color2):
        types.append("warm_cold")

    # Same family check (same color group)
    if ColorUtilsExtended.is_same_family(color1, color2):
        types.append("same_family")

    # Warm pair check
    if ColorUtilsExtended.is_warm_pair(color1, color2):
        types.append("warm_pair")

    # Cold pair check
    if ColorUtilsExtended.is_cold_pair(color1, color2):
        types.append("cold_pair")

    # Pastel pair check
    if ColorUtilsExtended.is_pastel_pair(color1, color2):
        types.append("pastel_pair")

    # Vivid pair check
    if ColorUtilsExtended.is_vivid_pair(color1, color2):
        types.append("vivid_pair")

    return types


def generate_color_combinations():
    NAMED_COLORS = list(mcolors.CSS4_COLORS)
    combinations = []

    for color1 in NAMED_COLORS:
        for color2 in NAMED_COLORS:
            if color1 == color2:
                continue

            contrast = round(ColorUtils.contrast_ratio(color1, color2), 2)

            if contrast > 0:
                types = detect_combination_types(color1, color2, contrast)

                combinations.append({
                    "color1": color1,
                    "color2": color2,
                    "contrast": contrast,
                    "types": types
                })

    return combinations


def main():
    logger.info("Exporting color combinations...")
    combinations = generate_color_combinations()

    logger.info(f"Total combinations found: {len(combinations)}")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(combinations, f, indent=4)

    logger.info(f"Exported to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

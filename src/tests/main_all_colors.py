from matplotlib import colors as mcolors

from color_utils import ColorUtils

NAMED_COLORS = list(mcolors.CSS4_COLORS)
valid_contrasts = []

for text_color in NAMED_COLORS:
    for background_color in NAMED_COLORS:
        if text_color != background_color:
            contrast = round(ColorUtils.contrast_ratio(text_color, background_color), 2)
            if contrast > 2:
                valid_contrasts.append((text_color, background_color))

print(len(valid_contrasts))

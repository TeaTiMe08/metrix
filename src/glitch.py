class Glitch:
    """Class to track the glitch states of characters."""

    def __init__(self, position, original_char, restore_frame):
        self.position = position
        self.original_char = original_char
        self.restore_frame = restore_frame

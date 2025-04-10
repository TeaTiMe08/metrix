#!/usr/bin/env python3
"""
Test script for validating all color configuration combinations in Metrix.
This script tests various combinations of TEXT_COLOR and BACKGROUND_COLOR settings
to verify they work correctly with the resolve_colors method.
"""

import os
import shutil
import sys
import tempfile
import time
import uuid
from pathlib import Path

from color_utils import ColorUtils
from frame_builder import FrameBuilder
from gif_builder import GifBuilder
from log_config import logger

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ColorConfigTester:
    """Class to test all possible color configuration combinations."""

    def __init__(self):
        """Initialize the tester with color options."""
        self.color_options = [
            "random",
            "random-light",
            "random-dark",
            "complementary",
            "contrasting",
            "shade",
            "red",  # Example of a named color
            "blue"  # Example of another named color
        ]

        self.minimum_contrasts = [2, 3, 4]
        self.results = []
        self.output_dir = Path("output/color_tests")

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def run_tests(self):
        """Run tests for all combinations of text and background color configurations."""
        logger.info(f"Starting color configuration tests... Output directory: {self.output_dir}")

        # Test all combinations - first resolve colors without rendering
        for text_color in self.color_options:
            for bg_color in self.color_options:
                for contrast in self.minimum_contrasts:
                    self._test_combination(bg_color, text_color, contrast)

        # Print results in table format before generating GIFs
        self._print_results()

        # Now generate the GIFs for each combination
        logger.info("")
        logger.info("Generating visualization GIFs for all combinations...")
        for result in self.results:
            if "ERROR" not in result["Result Text"]:  # Only render successful combinations
                result["GIF Path"] = self._render_combination(
                    result["BG Config"], result["Text Config"], result["Min Contrast"],
                    result["Result BG"], result["Result Text"], result["Method"],
                    result["Actual Contrast"], result["Modulation"]
                )
                logger.info(f"Generated GIF: {result['GIF Path']}")

        # Print final results with GIF paths
        logger.info("All tests and renderings complete.")
        self._print_results()

    def _test_combination(self, bg_color, text_color, min_contrast):
        """Test a specific combination of text color, background color, and minimum contrast."""
        try:
            logger.info(f"_______________________________________________________________________________________________________________________")
            logger.info("|                                                                                                                      |")
            logger.info(f"| TEST START: BG:{bg_color}, TXT:{text_color}, Min Contrast:{min_contrast}")
            logger.info("|")
            result_bg, result_text, method, contrast, modulation = ColorUtils.resolve_colors(
                bg_color, text_color, min_contrast
            )

            method = method if method is not '' else 'None'
            modulation = modulation if modulation is not '' else 'None'

            # Add to results without generating GIF yet
            self.results.append({
                "Text Config": text_color,
                "BG Config": bg_color,
                "Min Contrast": min_contrast,
                "Result BG": result_bg,
                "Result Text": result_text,
                "Method": method,
                "Actual Contrast": contrast,
                "Modulation": modulation,
                "GIF Path": "Pending"  # Will be updated later
            })

            # Log individual result
            logger.info("|")
            logger.info(f"| TEST RESULT: BG:{result_bg}, TXT:{result_text}, Method:{method}, Contrast:{contrast}, Modulation:{modulation}")
            logger.info("|______________________________________________________________________________________________________________________|")

        except Exception as e:
            logger.error(f"Error testing {text_color} + {bg_color}: {str(e)}")
            self.results.append({
                "BG Config": bg_color,
                "Text Config": text_color,
                "Min Contrast": min_contrast,
                "Result BG": "ERROR",
                "Result Text": "ERROR",
                "Method": "ERROR",
                "Actual Contrast": str(e),
                "Modulation": "ERROR",
                "GIF Path": "ERROR"
            })

    def _render_combination(self, bg_config, text_config, min_contrast, result_bg, result_text, method, contrast, modulation):
        """Render a GIF for the given color combination."""
        try:
            # Create a unique identifier and filename
            filename = f"{bg_config}_{text_config}_{result_bg}_{result_text}.gif"
            output_path = os.path.join(self.output_dir, filename)

            # Create a unique working directory
            frames_dir = tempfile.mkdtemp(prefix=f"metrix_test_{uuid.uuid4().hex}_")

            # Generate text describing the color configuration
            text_content = (
                f"Color Configuration Test\n"
                f"-----------------------\n\n"
                f"BG Config: {bg_config}\n"
                f"Text Config: {text_config}\n"
                f"Min Contrast: {min_contrast}\n\n"
                f"Method: {method}\n"
                f"Result BG: {result_bg}\n"
                f"Result Text: {result_text}\n"
                f"Contrast: {contrast}"
                f"Modulation: {modulation}\n\n"
            )

            # Split into lines
            text_lines = text_content.split('\n')

            # Generate frames using the FrameBuilder
            activity_graphic = ""  # No activity graphic needed
            frame_rate = 50  # Faster rendering

            # Create frames with actual colors from the test
            FrameBuilder.create_typing_frames(text_lines, activity_graphic,
                                              result_text, result_bg, frames_dir)

            # Generate the GIF
            GifBuilder.generate_gif_ffmpeg(frame_rate, output_path, frames_dir)

            # Cleanup temporary directory
            shutil.rmtree(frames_dir, ignore_errors=True)

            return output_path

        except Exception as e:
            logger.error(f"Error rendering GIF for {text_config} + {bg_config}: {str(e)}")
            return f"RENDER_ERROR: {str(e)}"

    def _print_results(self):
        """Print test results in a formatted table without using tabulate."""
        headers = ["BG Config", "Text Config", "Min Contrast",
                   "Result BG", "Result Text", "Method", "Actual Contrast", "Modulation", "GIF Path"]

        # Get maximum width for each column
        col_widths = [len(h) for h in headers]
        for result in self.results:
            for i, key in enumerate(headers):
                # Skip GIF path in width calculation (too long)
                if key == "GIF Path" and i == 8:
                    col_widths[i] = max(col_widths[i], 40)  # Cap at 40 chars
                else:
                    col_widths[i] = max(col_widths[i], len(str(result.get(key, ""))))

        # Create format string for rows
        fmt = " | ".join(f"{{:{w}}}" for w in col_widths)

        # Create separator line
        sep_line = "-+-".join("-" * w for w in col_widths)

        logger.info("")
        logger.info("=" * 80)
        logger.info("COLOR CONFIGURATION TEST RESULTS")
        logger.info("=" * 80)

        # Print headers
        logger.info(fmt.format(*headers))
        logger.info(sep_line)

        # Print data rows
        for result in self.results:
            values = [
                result["BG Config"],
                result["Text Config"],
                result["Min Contrast"],
                result["Result BG"],
                result["Result Text"],
                result["Method"],
                str(result["Actual Contrast"]),
                str(result["Modulation"]),
                str(result.get("GIF Path", ""))[:40]  # Truncate path if too long
            ]
            logger.info(fmt.format(*values))

        logger.info("=" * 80)
        logger.info(f"Total combinations tested: {len(self.results)}")
        logger.info(f"GIFs generated in: {self.output_dir}")

        # Summary of failures
        failures = [r for r in self.results if "ERROR" in str(r["Result Text"])]
        render_failures = [r for r in self.results if "RENDER_ERROR" in str(r.get("GIF Path", ""))]

        if failures:
            logger.info(f"COLOR FAILURES: {len(failures)} combinations failed")
            for f in failures:
                logger.info(f"- {f['BG Config']} + {f['Text Config']} ({f['Min Contrast']}): {f['Actual Contrast']}")

        if render_failures:
            logger.info(f"RENDER FAILURES: {len(render_failures)} combinations failed to render")
            for f in render_failures:
                logger.info(f"- {f['BG Config']} + {f['Text Config']} ({f['Min Contrast']}): {f['GIF Path']}")

        if not failures and not render_failures:
            logger.info("All combinations successful!")


def main():
    """Main entry point for the test script."""
    tester = ColorConfigTester()
    tester.run_tests()


if __name__ == "__main__":
    main()

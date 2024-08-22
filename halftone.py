from drawBot import *
from tile import Tile
import os
import time
import datetime
import json


class Halftone:
    """
    A class for creating a halftone effect using the DrawBot library.

    Args:
      path (str): The path to the image file.
      settings (dict): A dictionary of settings for the halftone effect.
    """

    def __init__(self, path, settings):

        self.path = path
        if not path:
            raise ValueError("Please provide a valid path to an image file.")

        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        self._update_settings(settings)

        if self.verbose:
            print("Settings:", self.settings)

        self._reescale_image()

        # Initialize the time taken attribute
        self.time_taken = 0
        start_time = time.time()

        # Draw the halftone effect
        self._draw()

        # Save the image as a PDF file
        if self.settings['save']:
            self._save_image()

        end_time = time.time()
        self.time_taken = end_time - start_time

        # Print the information about the image
        # if self.verbose:
        # print(f"Filename: {self.path} \nImage size: {self.w} x {self.h} \nResolution: {self.resolution} \nContrast: {self.contrast} \nAngle: {degrees(self.angle)} degrees \nUse honeycomb grid: {self.use_honeycomb_grid} \nReescale image: {self.reescale_image}")
        # print(f"Time taken: {self.time_taken:.2f} seconds")

    def _update_settings(self, settings):
        """
        Updates the settings with the default settings.

        Args:
          settings (dict): The settings to update.
        """
        self.settings = settings

        self.verbose = self.settings['verbose']
        self.settings['color'] = list(
            map(lambda x: x / 255, self.settings['color'])
        )  # Convert color values to the range [0, 1]

    def _map_range(self, value, start1, stop1, start2, stop2):
        return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2

    def _reescale_image(self):
        image_width, image_height = imageSize(self.path)
        if not self.settings['reescale_image']:
            self.w, self.h = image_width, image_height
        else:
            self.im = ImageObject()

            with self.im:
                size(image_width, image_height)
                image(self.path, (0, 0))

            scale_factor = min(595 / image_width, 842 / image_height)
            self.im.lanczosScaleTransform(scale=scale_factor, aspectRatio=None)
            self.w, self.h = 595, 842
    
    def _save_image(self):
        """
        Saves the halftone effect as a PDF file.
        """
        output_dir = './output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate the current date and time string
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        ext = self.settings['save_format']
        contrast = self.settings['contrast']
        resolution = self.settings['resolution']

        path = f'{output_dir}/halftone_{current_time}_resolution-{resolution}_contrast-{contrast}.{ext}'
        saveImage(path)

        if self.verbose:
            print(f"Image saved to: {path}")

    def _drawTile(self, width, height, radius):
        """
        Draws a single tile with the specified width, height, and radius.

        Args:
          width (int): The width of the tile.
          height (int): The height of the tile.
          radius (int): The radius of the tile.
        """
        self.tile = Tile(width, height, radius)
        self.tile.setPath(x, y)
        self.tile.drawPath()

    def _draw(self):
        """
        Draws the halftone effect on the canvas.
        """
        contrast = self.settings['contrast']
        honeycomb = self.settings['use_honeycomb_grid']
        reescale_image = self.settings['reescale_image']
        is_inverse = self.settings['inverse']
        resolution = self.settings['resolution']

        if self.settings['reescale_image']:
            newPage(595, 842)
        else:
            newPage(self.w, self.h)

        if self.settings['color_mode'] == 'cmyk':
            cmykFill(*self.settings['color'])
        else:
            fill(*self.settings['color'])

        # Get the image size and calculate the dot size
        dot_size = min(self.w, self.h) // resolution
        dot_min_size = self.settings['dot_min_size']
        dot_spacing = max(self.w, self.h) // resolution

        translate(-dot_size / 2, -dot_size / 2)

        # Expand grid bounds to account for rotation
        expanded_res = int(resolution * 1.5)

        for width in range(-expanded_res, expanded_res):
            for height in range(-expanded_res, expanded_res):
                # Original grid position
                x = dot_spacing + width * dot_spacing
                y = dot_spacing + height * dot_spacing

                # Apply honeycomb effect
                if honeycomb:
                    x += (height & 1) * (dot_spacing // 2)

                # Rotate dot position by the specified angle around the center of the image
                angle = self.settings['angle']
                center_x, center_y = self.w / 2, self.h / 2
                x_rot = (x - center_x) * cos(angle) - \
                    (y - center_y) * sin(angle) + center_x
                y_rot = (x - center_x) * sin(angle) + \
                    (y - center_y) * cos(angle) + center_y

                # Sample the color using the rotated position
                if not (0 <= x_rot < self.w and 0 <= y_rot < self.h):
                    continue

                if reescale_image:
                    color = imagePixelColor(self.im, (x_rot, y_rot))
                else:
                    color = imagePixelColor(self.path, (x_rot, y_rot))

                if not color:
                    continue

                r, g, b, a = color

                # Only draw if RGB value is different from 0
                # if not (r > 0 or g > 0 or b > 0):
                #   continue

                average_color = (r + g + b) / 3

                # Define a new dot_size based on red value
                range_start = 1 - 2 * is_inverse  # 1 if inverse, -1 if not
                range_end = is_inverse  # 0 if inverse, 1 if not
                new_dot_size = self._map_range(
                    average_color, range_start, range_end, dot_min_size, dot_size) * contrast

                # Don't draw if new_dot_size is small or equal to the size threshold
                # if new_dot_size <= self.size_threshold:
                #   continue

                # if self.verbose:
                #   print(f"Drawing dot at ({x_rot:.2f}, {y_rot:.2f}) with size {new_dot_size:.2f}")

                oval(x_rot - new_dot_size / 2, y_rot - new_dot_size / 2,
                     new_dot_size, new_dot_size)

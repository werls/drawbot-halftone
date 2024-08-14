from drawBot import *
from tile import Tile
import os
import time
import datetime


class Halftone:
    """
    A class for creating a halftone effect using the DrawBot library.

    Args:
      path (str): The path to the image file.
      resolution (int, optional): The resolution of the halftone grid. Defaults to 100.
      contrast (float, optional): The contrast of the halftone dots. Defaults to 1.
      angle (float, optional): The angle of rotation for the halftone dots in radians. Defaults to radians(45).
    """

    def __init__(self, path, settings):

        self.path = path
        if not path:
            raise ValueError("Please provide a valid path to an image file.")

        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        self.default_settings = {
            'resolution': 100,
            'contrast': 1,
            'angle': radians(45),
            'verbose': True,
            'save': True,
            'use_honeycomb_grid': True
        }

        self._updateSettings(settings)

        # Get the image size and calculate the dot size
        self.w, self.h = imageSize(self.path)
        self.dot_size = min(self.w, self.h) // self.resolution

        # Initialize the time taken attribute
        self.time_taken = 0

        # Draw the halftone effect
        start_time = time.time()
        self._draw()
        end_time = time.time()
        self.time_taken = end_time - start_time

        # Save the image as a PDF file
        if self.save:
            self._save_image()

        # Print the information about the image
        if self.verbose:
            print(f"Filename: {self.path} \nImage size: {self.w} x {self.h} \nResolution: {self.resolution} \nContrast: {self.contrast} \nAngle: {degrees(self.angle)} degrees")
            print(f"Time taken: {self.time_taken:.2f} seconds")

    def _updateSettings(self, settings):
        """
        Updates the settings with the default settings.

        Args:
          settings (dict): The settings to update.
        """
        self.settings = self.default_settings.copy()
        self.settings.update(settings)

        self.resolution = self.settings['resolution']
        self.contrast = self.settings['contrast']
        self.angle = self.settings['angle']
        self.verbose = self.settings['verbose']
        self.save = self.settings['save']
        self.use_honeycomb_grid = self.settings['use_honeycomb_grid']

    def _map_range(self, value, start1, stop1, start2, stop2):
        return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2

    def _save_image(self):
        """
        Saves the halftone effect as a PDF file.
        """
        output_dir = './output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate the current date and time string
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = f'{output_dir}/reticulate_{current_time}_resolution-{self.resolution}_contrast-{self.contrast}.pdf'
        saveImage(path)

        # os.system(f'open --background -a Preview {path}')

    def _drawTile(self, width, height, radius):
        """
        Sets the tile size for the halftone effect.

        Args:
          width (int): The width of the tile.
          height (int): The height of the tile.
        """
        self.tile = Tile(width, height, radius)
        self.tile.setPath(x, y)
        self.tile.drawPath()

    def _draw(self):
        """
        Draws the halftone effect on a new page.
        """

        newPage(self.w, self.h)
        fill(0)
        translate(-self.dot_size / 2, -self.dot_size / 2)

        dot_spacing = max(self.w, self.h) // self.resolution

        # Expand grid bounds to account for rotation
        expanded_res = int(self.resolution * 1.5)

        for width in range(-expanded_res, expanded_res):
            for height in range(-expanded_res, expanded_res):
                # Original grid position
                x = dot_spacing + width * dot_spacing
                y = dot_spacing + height * dot_spacing\

                # Apply honeycomb effect
                if self.use_honeycomb_grid:
                    x += (height & 1) * (dot_spacing // 2)

                # Rotate dot position by the specified angle around the center of the image
                center_x, center_y = self.w / 2, self.h / 2
                x_rot = (x - center_x) * cos(self.angle) - \
                    (y - center_y) * sin(self.angle) + center_x
                y_rot = (x - center_x) * sin(self.angle) + \
                    (y - center_y) * cos(self.angle) + center_y

                # Sample the color using the rotated position
                if 0 <= x_rot < self.w and 0 <= y_rot < self.h:
                    color = imagePixelColor(self.path, (x_rot, y_rot))

                    if color:
                        r, g, b, a = color

                        # Only draw if RGB value is different from 0
                        if r > 0 or g > 0 or b > 0:
                            average_color = (r + g + b) / 3

                            # Define a new dot_size based on red value
                            new_dot_size = self._map_range(
                                average_color, 1, 0, 0, self.dot_size) * self.contrast

                            # Don't draw if new_dot_size is small or equal to 0
                            if new_dot_size > 0:
                                # t = Tile(self.dot_size * 2, self.dot_size * 2, self._map_range(new_dot_size, 0, self.dot_size, 0, 1))
                                # t = Tile(self.dot_size * 2, self.dot_size * 2, 1)
                                # t.setPath(x_rot, y_rot)
                                # t.drawPath()
                                oval(x_rot - new_dot_size / 2, y_rot - new_dot_size / 2,
                                     new_dot_size, new_dot_size)

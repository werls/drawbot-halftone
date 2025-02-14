from drawBot import *
# from src.tile import Tile
import os
import time
import datetime
# import json

class Halftone:
    """
    A class for creating a halftone effect using the DrawBot library.

    Args:
      path (str): The path to the image file.
      settings (dict): A dictionary of settings for the halftone effect.
    """

    def __init__(self, path, settings):
        self._validate_path(path)
        self.path = path
        self.verbose = True
        self.settings = settings
        
        self._update_settings(settings)
        self._reescale()
        
        if self.verbose:
          self._print_settings()
        
        elapsed_time = 0
        start_time = time.time() # Keeps track of the time taken to draw the image

        self._draw()
        if self.settings['save']:
            output_dir = self.settings['output_dir'] or './output'
            keep_original_name = self.settings['keep_original_name']

            self._save_image(output_dir, keep_original_name)

        elapsed_time = time.time() - start_time
        print(f"Time taken: {elapsed_time:.2f} seconds")

        # Print the information about the image
        # if self.verbose:
        # print(f"Filename: {self.path} \nImage size: {self.w} x {self.h} \nResolution: {self.resolution} \nContrast: {self.contrast} \nAngle: {degrees(self.angle)} degrees \nUse honeycomb grid: {self.use_honeycomb_grid} \nReescale image: {self.reescale}")

    def _validate_path(self, path):
        """
        Validates the path to the image file.

        Args:
          path (str): The path to the image file.
        """
        if not path:
            raise ValueError("Please provide a valid path to an image file.")

        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

    def _update_settings(self, settings):
        """
        Updates the settings with the default settings.

        Args:
          settings (dict): The settings to update.
        """
        # self.settings = settings
        self.verbose = self.settings['verbose']

        # Convert color values to the range [0, 1]
        # to match the Drawbot's fill() function
        if self.settings['color_mode'] == 'rgba':
          self.settings['color'] = [x / 255 for x in settings['color']]
        elif self.settings['color_mode'] == 'cmyk':
          self.settings['color'] = [x / 100 for x in settings['color']]
        else:
          raise ValueError("Invalid color mode. Please use 'rgba' or 'cmyk'.")

    def _reescale(self):
        image_width, image_height = imageSize(self.path)

        if not self.settings['reescale']:
            self.w, self.h = image_width, image_height
        else:
            self.im = ImageObject()
            with self.im:
                size(image_width, image_height)
                image(self.path, (0, 0))

            scale_factor = min(595 / image_width, 842 / image_height)
            self.im.lanczosScaleTransform(scale=scale_factor, aspectRatio=None)
            self.w, self.h = 595, 842

    def _print_settings(self):
        """
        Prints the settings for the halftone effect.
        """
        for key, value in self.settings.items():
            formatted_key = key.replace('_', ' ').capitalize()
            print(f"{formatted_key}: {value}")
        print("-")

    def _save_image(self, output_dir='./output', keep_original_name=False):
        """
        Saves the halftone effect as a PDF file.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ext = self.settings['output_format']
        contrast = self.settings['contrast']
        resolution = self.settings['resolution']

        if keep_original_name:
            filename = os.path.basename(self.path)
            name, _ = os.path.splitext(filename)
            path = f'{output_dir}/{name}_halftone_{current_time}_resolution-{resolution}_contrast-{contrast}.{ext}'
        else:
            path = f'{output_dir}/halftone_{current_time}_resolution-{resolution}_contrast-{contrast}.{ext}'
            
        saveImage(path)

        if self.verbose:
            print(f"Image saved to: {path}")
    
    # def _drawTile(self, width, height, radius):
    #     """
    #     Draws a single tile with the specified width, height, and radius.

    #     Args:
    #       width (int): The width of the tile.
    #       height (int): The height of the tile.
    #       radius (int): The radius of the tile.
    #     """
    #     self.tile = Tile(width, height, radius)
    #     self.tile.setPath(x, y)
    #     self.tile.drawPath()

    def _draw(self):
        """
        Draws the halftone effect on the canvas.
        """
        contrast = self.settings['contrast']
        honeycomb = self.settings['use_honeycomb_grid']
        reescale = self.settings['reescale']
        is_inverse = self.settings['inverse']
        resolution = self.settings['resolution']
        angle = self.settings['angle']

        if self.settings['reescale']:
            newPage(595, 842) # need to correct this magic number
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
                center_x, center_y = self.w / 2, self.h / 2
                dx, dy = x - center_x, y - center_y
                x_rot = dx * cos(angle) - dy * sin(angle) + center_x
                y_rot = dx * sin(angle) + dy * cos(angle) + center_y

                # Sample the color using the rotated position
                if not (0 <= x_rot < self.w and 0 <= y_rot < self.h):
                    continue
                
                color = imagePixelColor(
                    self.im if reescale else self.path, (x_rot, y_rot)
                    )
                if not color: continue
                r, g, b, a = color

                # Only draw if RGB value is different from 0
                # if not (r > 0 or g > 0 or b > 0):
                #   continue

                average_color = (r + g + b) / 3

                # Define a new dot_size based on red value
                range_start = 1 - 2 * is_inverse  # 1 if inverse, -1 if not
                range_end = is_inverse  # 0 if inverse, 1 if not
                new_dot_size = self._map_range(
                    average_color, 
                    range_start, range_end, 
                    dot_min_size, dot_size
                    ) * contrast

                # Don't draw if new_dot_size is small or equal to the size threshold
                # if new_dot_size <= self.size_threshold:
                #   continue

                # if self.verbose:
                #   print(f"Drawing dot at ({x_rot:.2f}, {y_rot:.2f}) with size {new_dot_size:.2f}")

                oval(
                    x_rot - new_dot_size / 2, y_rot - new_dot_size / 2,
                    new_dot_size, new_dot_size
                    )

    def _map_range(self, value, start1, stop1, start2, stop2):
            return (value - start1) / (stop1 - start1) * (stop2 - start2) + start2
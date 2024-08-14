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
    settings (dict): A dictionary of settings for the hal
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
      'size_threshold': 1,
      'verbose': True,
      'save': True,
      'use_honeycomb_grid': True,
      'reescale_image': False,
      'default_size': (595, 842)
    }
    
    self._updateSettings(settings)

    # Get the image size
    image_width, image_height = imageSize(self.path)
    
    if not self.settings['reescale_image']:
      self.w, self.h = image_width, image_height
    else:
      self.im = ImageObject()
      
      with self.im:
        size(image_width, image_height)
        image(path, (0, 0))
      
      scale_factor = min(595 / image_width, 842 / image_height)
      self.im.lanczosScaleTransform(scale=scale_factor, aspectRatio=None)

      self.w, self.h = 595, 842

    # Get the image size and calculate the dot size
    self.dot_size = min(self.w, self.h) // self.resolution
    
    # Initialize the time taken attribute
    self.time_taken = 0
    start_time = time.time()
    
    # Draw the halftone effect
    self._draw()

    # Save the image as a PDF file
    if self.save:
      self._save_image()

    end_time = time.time()
    self.time_taken = end_time - start_time

    # Print the information about the image
    if self.verbose:
      print(f"Filename: {self.path} \nImage size: {self.w} x {self.h} \nResolution: {self.resolution} \nContrast: {self.contrast} \nAngle: {degrees(self.angle)} degrees \nSize threshold: {self.size_threshold} \nUse honeycomb grid: {self.use_honeycomb_grid} \nReescale image: {self.reescale_image}")
      print(f"Time taken: {self.time_taken:.2f} seconds")

  def _updateSettings(self, settings):
      """
      Updates the settings with the default settings.
      
      Args:
        settings (dict): The settings to update.
      """
      # Print default settings and incoming settings for debugging
      # print("Default settings:", self.default_settings)
      # print("Incoming settings:", settings)
      
      # Merge default settings with the provided settings
      self.settings = {**self.default_settings, **settings}

      # Print the merged settings to verify the update
      # print("Merged settings:", self.settings)
      
      self.resolution = self.settings['resolution']
      self.contrast = self.settings['contrast']
      self.angle = self.settings['angle']
      self.size_threshold = self.settings['size_threshold']
      self.verbose = self.settings['verbose']
      self.save = self.settings['save']
      self.use_honeycomb_grid = self.settings['use_honeycomb_grid']
      self.reescale_image = self.settings['reescale_image']
  
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
    
    if self.reescale_image:
      newPage(595, 842)
    else:
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
        y = dot_spacing + height * dot_spacing
        
        # Apply honeycomb effect
        if self.use_honeycomb_grid:
          x += (height & 1) * (dot_spacing // 2)
          
        # Rotate dot position by the specified angle around the center of the image
        center_x, center_y = self.w / 2, self.h / 2
        x_rot = (x - center_x) * cos(self.angle) - (y - center_y) * sin(self.angle) + center_x
        y_rot = (x - center_x) * sin(self.angle) + (y - center_y) * cos(self.angle) + center_y

        # Sample the color using the rotated position
        if not (0 <= x_rot < self.w and 0 <= y_rot < self.h):
          continue

        if self.settings['reescale_image']:
          color = imagePixelColor(self.im, (x_rot, y_rot))
        else:
          color = imagePixelColor(self.path, (x_rot, y_rot))

        if not color:
          continue
        
        r, g, b, a = color
        
        # Only draw if RGB value is different from 0
        if not (r > 0 or g > 0 or b > 0):
          continue
        
        average_color = (r + g + b) / 3
        
        # Define a new dot_size based on red value
        new_dot_size = self._map_range(average_color, 1, 0, 0, self.dot_size) * self.contrast
        
        # Don't draw if new_dot_size is small or equal to the size threshold
        if new_dot_size <= self.size_threshold:
          continue
        
        # t = Tile(self.dot_size * 2, self.dot_size * 2, self._map_range(new_dot_size, 0, self.dot_size, 0, 1))
        # t = Tile(self.dot_size * 2, self.dot_size * 2, 1)
        # t.setPath(x_rot, y_rot)
        # t.drawPath()
        oval(x_rot - new_dot_size / 2, y_rot - new_dot_size / 2,
            new_dot_size, new_dot_size)
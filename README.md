# Reticulate

This is an evolution of my own [basic halftone effect](https://github.com/werls/basic-drawbot-halftone) using [Drawbot](https://www.drawbot.com/).

## How to

## Parameters

| Parameter       | Type    | Description                                      | Default |
|-----------------|---------|--------------------------------------------------|---------|
| --path          | string  | The path to the image file.                      | None    |
| --resolution    | int     | The resolution of the halftone grid.             | 100     |
| --contrast      | float   | The maximum size of the halftone dots.           | 1       |
| --angle         | float   | The angle of rotation for the halftone grid.     | 45      |
| --color         | string  | The color of the halftone dots.                  | 0,0,0,1 |
| --color_mode    | string  | The color mode of the halftone dots (rgba or cmyk). | rgba |
| --honeycomb     | bool    | Use a honeycomb grid instead of a square grid.   | True    |
| --reescale_image| bool    | Reescale the image to fit the canvas default size. | False |
| --inverse       | bool    | Invert the colors of the image.                  | False   |
| --save          | bool    | Save the image to a file in /output/ folder.     | True    |
| --preset        | string  | A JSON string or file path of settings for the halftone effect. | None |
| --verbose       | bool    | Print the settings of the halftone effect.       | True    |


## Example


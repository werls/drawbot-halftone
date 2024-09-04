import argparse
import json
from math import radians
from drawBot import newDrawing, endDrawing
from src.halftone import Halftone

def str2bool(v):
    return v.lower() in ('true', '1', 'yes')

def main():
    parser = argparse.ArgumentParser(description='Create a halftone effect using the DrawBot library.')
    
    parser.add_argument('positional_path', nargs='?', help='The path to the image file.')
    parser.add_argument('--path', type=str, nargs='?', help='The path to the image file.')
    parser.add_argument('--resolution', '-r', type=int, nargs='?', default=100,
                        help='The resolution of the halftone grid. Defaults to 100.')
    parser.add_argument('--contrast', '-c', type=float, nargs='?', default=1,
                        help='The contrast of the halftone dots. Defaults to 1.')
    parser.add_argument('--dot-min-size', type=float, nargs='?', default=0,
                        help='The minimum size of the halftone dots. Defaults to 0')
    parser.add_argument('--angle', type=float, nargs='?', default=45,
                        help='The angle of rotation for the halftone dots in degrees. Defaults to 45.')
    parser.add_argument('--verbose', type=str2bool, nargs='?', const=True, default=True,
                        help='Enable verbose output. Defaults to True.')
    # parser.add_argument('--save', type=str2bool, nargs='?', const=True, default=True,
    #                     help='Save the image as a file. Defaults to True.')
    parser.add_argument('--honeycomb', type=str2bool, nargs='?', const=True, default=True,
                        help='Use a honeycomb grid. Defaults to True.')
    parser.add_argument('--reescale', type=str2bool, nargs='?', const=True, default=False,
                        help='Rescale the image to fit the page. Defaults to False.')
    parser.add_argument('--inverse', type=str2bool, nargs='?', const=True, default=False,
                        help='Invert the color. Defaults to False.')
    parser.add_argument('--preset', '-p', type=str, nargs='?',
                        help='A JSON string or file path of settings for the halftone effect.')
    parser.add_argument('--color', type=str, nargs='?',
                        help='The color of the halftone dots in RGBA or CMYK format.', default='0,0,0,255')
    parser.add_argument('--color-mode', type=str, nargs='?',
                        help='The color mode of the halftone dots. (rgba or cmyk)', default='rgba')
    parser.add_argument('--output-format', type=str, nargs='?',
                        help='The format of the saved image. (pdf, png, jpg)', default='pdf')
    parser.add_argument('--output-dir', "-o", type=str, nargs='?', help='The directory to save the image file.')
    parser.add_argument('--keep-original-name', '-k', type=str2bool, nargs='?', const=True, default=False,
                        help='Keep the original name of the image file. Defaults to False.')

    args = parser.parse_args()
    path = args.path or args.positional_path

    settings = {
        'resolution': args.resolution,
        'contrast': args.contrast,
        'angle': radians(args.angle),
        'verbose': args.verbose,
        # 'save': args.save, # CLI use should always save the image
        'save': True,
        'use_honeycomb_grid': args.honeycomb,
        'reescale': args.reescale,
        'inverse': args.inverse,
        'color': [float(c) for c in args.color.split(',')],
        'color_mode': args.color_mode,
        'dot_min_size': args.dot_min_size,
        'output_format': args.output_format,
        'output_dir': args.output_dir,
        'keep_original_name': args.keep_original_name
    }

    print(args.color_mode)

    if args.preset:
        # incluir uma checagem para verificar se o path é válido

        try:
            with open(args.preset, 'r') as file:
                preset = json.load(file)
            settings.update(preset)
        except FileNotFoundError:
            settings.update(json.loads(args.preset))

    newDrawing()
    halftone = Halftone(path, settings)
    endDrawing()

if __name__ == '__main__':
    main()
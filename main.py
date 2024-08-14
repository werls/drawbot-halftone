import argparse
from math import radians
from drawBot import newDrawing, endDrawing
from halftone import Halftone

def main():
    parser = argparse.ArgumentParser(
        description='Create a halftone effect using the DrawBot library.')
    parser.add_argument('path', type=str, help='The path to the image file.')
    parser.add_argument('--resolution', type=int, default=256,
                        help='The resolution of the halftone grid. Defaults to 100.')
    parser.add_argument('--contrast', type=float, default=1,
                        help='The contrast of the halftone dots. Defaults to 1.')
    parser.add_argument('--angle', type=float, default=45,
                        help='The angle of rotation for the halftone dots in degrees. Defaults to 45.')
    parser.add_argument('--verbose', type=bool, default=True,
                        help='Enable verbose output. Defaults to True.')
    parser.add_argument('--save', type=bool, default=True,
                        help='Save the image as a PDF file. Defaults to True.')
    parser.add_argument('--honeycomb', type=bool, default=True,
                        help='Use a honeycomb grid. Defaults to True.')

    args = parser.parse_args()

    # Convert angle to radians
    angle_in_radians = radians(args.angle)

    newDrawing()

    # Instantiate and run the Reticulate class
    halftone = Halftone(
        path=args.path,
        resolution=args.resolution,
        contrast=args.contrast,
        angle=angle_in_radians,
        verbose=args.verbose,
        save=args.save,
        honeycomb=args.honeycomb
    )

    endDrawing()


if __name__ == '__main__':
    main()

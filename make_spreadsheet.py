#!/usr/bin/env python3

import argparse
import csv
from PIL import Image


def setup_args():
    parser = argparse.ArgumentParser(description='Convert an image to a spreadsheet of RGB values')
    
    parser.add_argument('--width', 
                        type=int,
                        default=32,
                        help='Output image width in cell columns')
    parser.add_argument('--height',
                        type=int,
                        default=24,
                        help='Output image height in 3x cell rows')
    parser.add_argument('image_path',
                        metavar='image',
                        help='Input image file path')
    parser.add_argument('output',
                        type=argparse.FileType('w'),
                        help='Output image file path')


    return parser


def main():
    parser = setup_args()
    context = parser.parse_args()
    
    with Image.open(context.image_path) as image:
        csv_writer = csv.writer(context.output)

        rgb_image = image.convert('RGB')
        image.resize((context.width, context.height))

        rows_count = 0
        for i in range(context.height):
            row = [rgb_image.getpixel((i, j)) for j in range(context.width)]
            rgb_rows = zip(*row)
            
            for rgb_row in rgb_rows:
                csv_writer.writerow(rgb_row)
                rows_count += 1

    print('Wrote {0} rows to {1}'.format(rows_count, context.output.name))

if __name__ == '__main__':
    main()

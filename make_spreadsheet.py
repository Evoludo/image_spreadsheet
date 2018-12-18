#!/usr/bin/env python3

import argparse
import csv
import xlsxwriter
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
    parser.add_argument('--no-formatting',
                        default=False,
                        action='store_true',
                        help='Don\'t use conditional formatting in spreadsheet, instead just output the numbers themselves')
    parser.add_argument('image_path',
                        metavar='image',
                        help='Input image file path')
    parser.add_argument('output',
                        help='Output image file path')


    return parser


def main():
    parser = setup_args()
    context = parser.parse_args()
    
    with xlsxwriter.Workbook(context.output) as wb:
        ws = wb.add_worksheet()
        ws.set_column(0, context.width, 4)

        red_format = {
            'type': '2_color_scale',
            'min_value': 0,
            'max_value': 255,
            'min_color': '#000000',
            'max_color': '#FF0000'
        }

        green_format = {
            'type': '2_color_scale',
            'min_value': 0,
            'max_value': 255,
            'min_color': '#000000',
            'max_color': '#00FF00'
        }

        blue_format = {
            'type': '2_color_scale',
            'min_value': 0,
            'max_value': 255,
            'min_color': '#000000',
            'max_color': '#0000FF'
        }

        formats = {
            0: red_format,
            1: green_format,
            2: blue_format
        }

        if not context.no_formatting:
            for r in range(context.height * 3):
                ws.conditional_format(r, 0, r, context.width, formats[r % 3])

        with Image.open(context.image_path) as image:
            rgb_image = image.convert('RGB')
            rgb_image = rgb_image.resize((context.width, context.height))

            rows_count = 0
            for i in range(context.height):
                row = [rgb_image.getpixel((j, i)) for j in range(context.width)]
                rgb_rows = zip(*row)
                
                for rgb_row in rgb_rows:
                    ws.write_row('A' + str(rows_count + 1), rgb_row)
                    rows_count += 1

    print('Wrote {0} rows to {1}'.format(rows_count, context.output))

if __name__ == '__main__':
    main()

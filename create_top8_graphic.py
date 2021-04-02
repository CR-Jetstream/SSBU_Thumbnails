"""
Script to create Top 8 Graphic  for Smash Ultimate

1. Read in the names file to event information and player placements

2. Have a blank graphic ready to populate the information

3. Have the script read in the character and add them to the graphic

4. Have the script open the graphic and add the information

7. Have the script output the images in a specified File location
"""

import io
import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import populate_globals

import sys
import getopt

'''Global Variables used in script'''
# Dictionaries for lookups
_character_database = {}
_player_database = {}
# Dictionary for global properties
_properties = dict()


class GraphicPlacement:
    def __init__(self, _place, _player, _twitter, _char_list):
        self.p = _place
        self.p1 = _player
        self.tw = _twitter
        self.c1 = _char_list
        self.c1_renders = []
        self.Images = []


def main(argv):
    event = 'Sample'
    number = 'Test'
    property_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "he:n:p:o:", ["event=", "number=", "property_file=", "output_file="])
    except getopt.GetoptError:
        print('create_top8_graphic.py -i <input_file>, -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('create_top8_graphic.py -i <input_file>, -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--input"):
            event = arg
        elif opt in ("-o", "--output_file"):
            output_file = arg
    # End of Command Line Arguments

    # 0. Setup information
    # Event
    global _properties
    _properties = setGlobals(event, number, property_file)
    # Read Player Database and Character Database
    global _character_database
    _character_database = populate_globals.readCharDatabase('Character_Database.csv', )
    global _player_database
    _player_database = populate_globals.readPlayerDatabase('Player_Database.csv', char_database=_character_database)
    # 1. Read in the input file to get event info and player names
    event_info, event_placements_lines = readGrpahicLines(_properties['top8_info'])
    # create list of placements
    event_placements = createPlacments(event_placements_lines)
    # 2. Have a blank graphic ready to populate the information
    back_image = Image.open(_properties['background_file'])
    # back_image.show()
    front_image = Image.open(_properties['foreground_file'])
    # front_image.show()
    # 3. Have the script read in the character and add them to the graphic
    event_graphic = createGraphic(event_info, event_placements, back_image, front_image)
    # 4. Save the images
    saveGraphic(event_graphic, _properties['save_location'])


if __name__ == "__main__":
    # Get command line inputs
    main(sys.argv[1:])
    print("Done")
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


def setGlobalsTop8(weekly, property_settings=None):
    """
    Set all globals based off the type of event. Weekly is the series.
    These globals are set to then create the associated thumbnails
    :param weekly:
    :param property_settings:
    :return:
    """
    # Set globals based off of type of weekly
    if weekly == 'Quarantainment':
        global_properties = populate_globals.setGlobalsQuarantainment_Top8()
    elif weekly == 'Students x Treehouse':
        global_properties = populate_globals.setGlobalsSxT_Top8()
    # elif weekly == 'Fro Fridays':
    #     global_properties = populate_globals.setGlobalsFro()
    # elif weekly == 'AWG':
    #     global_properties = populate_globals.setGlobalsAWG()
    # elif weekly == 'C2C Finale':
    #     global_properties = populate_globals.setGlobalsC2C()
    # elif weekly == 'Catman':
    #     global_properties = populate_globals.setGlobalsCatman()
    else:
        global_properties = {}
        # global_properties = populate_globals.set_default_properties_Top8()
    # return properties
    return global_properties


def readGrpahicLines(filename):
    """
    Open file and read it line by line
    return two items
        Dictionary of info - used for populating global information
        List of placements - used for creating individual graphic windows

    :param filename:
    :return:
    """
    # Open File
    file = io.open(filename, "r", encoding='utf8')
    file_text = file.readlines()
    # Filter through lines that matter:
    info_dict = {}
    placement_list = []
    for line in file_text:
        print("--- Reading Top 8 Lines ---")
        # check for format
        # {event_1} {round_1} - {player_1} ({char_1}) Vs {player_2} ({char_2}) - SSBU
        if line.startswith('#'):
            # Comment case
            continue
        # Strip new lines
        line = line.strip('\n')
        # Split line up by tabs
        line = line.split('\t')
        # Placements case - 1:, 2:, ..., 8:
        if len(line[0]) == 2 and line[0][1] == ':' and line[0][0] in '12345678':
            # Create placement from this information
            # place, name, twitter, characters
            a_placement = GraphicPlacement(_place=line[0][0], _player=line[1], _twitter=line[2], _char_list=line[3:])
            placement_list.append(a_placement)
        else:
            # Info cases
            # bring to lowercase to be easier to search later
            line[0] = line[0].lower()
            # Standard information
            if line[0] == 'event name:' or line[0] == 'event date:' or line[0] == 'entrants:':
                info_dict[line[0]] = line[1]
            # Media information
            elif line[0] == 'twitter:' or line[0] == 'youtube:' or line[0] == 'twitch:' or line[0] == 'bracket link:':
                info_dict[line[0]] = line[1]
            # Cases with more than one /t in the line
            # Set to watch information
            elif line[0] == 'Set to Watch:':
                # "Set to Watch:" : [set, player1, player2]
                info_dict[line[0]] = [line[1], line[2], line[3]]
    # end loop
    if len(placement_list) == 0 or len(info_dict.keys()) == 0:
        raise NameError("Filename " + filename + " was not properly read in")
    return info_dict, placement_list


def createPlacements(placements_list):
    """
    Take in a list of placements, and add character render file locations
    Writes out information to log file if present
    :param placements_list:
    :return:
    """
    # Read each line and grab information
    return_list = []

    # Loop through all matches and find character render file locations
    #  This involves looking at the Character and Player Databases to successfully grab the alts
    # Dictionaries for players and characters not found
    player_not_found = {}
    char_not_found = {}
    for a_placement in placements_list:
        # Loop through character lists and grab character render
        #  Add them to the new lists
        player_char_files = []
        for a_char in a_placement.c1:
            # Case for handling alts in the char name
            #  {event_1} {round_1} - {player_1} ({char_1}) Vs. {player_2} ({char_2}) - SSBU
            #  where {char_1[2]} = ["a_char a_alt", "a_char2 a_alt2", ...]
            alt_num_in_name = False
            if a_char[-2] == ' ' and a_char[-1] in "12345678":
                alt_num_in_name = True
                alt_num = '(' + a_char[-1] + ')'
                a_char = a_char[:-2]
            else:
                alt_num = '(1)'
            # Search for character in char database
            if a_char.upper() in _character_database.keys():
                a_char = _character_database[a_char.upper()]
            # Create char image file name
            char_file = a_char + ' ' + alt_num
            # Lookup character in player database for alt costume (if it exists) if alt not specified
            if not alt_num_in_name:
                player_name = a_placement.p1
                # Player not found case (to uppercase)
                if player_name.upper() not in _player_database.keys():
                    # add player to not found dictionary
                    if player_name not in player_not_found.keys():
                        player_not_found[player_name] = []
                    if a_char not in player_not_found[player_name]:
                        player_not_found[player_name].append(a_char)
                else:  # Player found, now look for characters
                    # Lookup character (to uppercase)
                    player_chars_lookup = _player_database[player_name.upper()]
                    char_found = False
                    # Search existing characters in player database
                    for p_char in player_chars_lookup:
                        if a_char.upper() in p_char.upper():
                            # Char found, set char file
                            char_file = p_char
                            char_found = True
                            break
                    # Char not found case and character is not random
                    if not char_found and a_char.upper() != 'RANDOM':
                        # add player to not found dictionary (to uppercase)
                        if player_name not in char_not_found.keys():
                            char_not_found[player_name] = []
                        if a_char not in char_not_found[player_name]:
                            char_not_found[player_name].append(a_char)
            # Check if char file exists at render location
            #  Render type must be specified, Render type 2 & 3 need not be
            if _properties['render_type'] is None:
                raise NameError("Error: 'render_type' is set to None")
            for rend_dir in [_properties['render_type'], _properties['render_type2'], _properties['render_type3']]:
                if rend_dir is None:
                    continue
                char_location = os.path.join(_properties['char_renders'], rend_dir, char_file + '.png')
                if not os.path.exists(char_location):
                    raise NameError("Character not found in " + a_placement.p + ": " + rend_dir + "/" + char_file)
            # Add to render files
            player_char_files.append(char_file)
        # end of placement loop

        # Add character renders to match
        a_placement.c1_renders = player_char_files
        # Add match to return list
        return_list.append(a_placement)
    # end of match loop

    # Write output information to log file - player and character not found information
    out_text = ""
    out_text += "** List of players not found **\n"
    for a_player in player_not_found.keys():
        out_text += "{s}".format(s=a_player)
        for a_char in player_not_found[a_player]:
            out_text += "\t{s}\t1".format(s=a_char)
        out_text += "\n"
    out_text += "** List of characters not found for players **\n"
    for a_player in char_not_found.keys():
        out_text += "{s}".format(s=a_player)
        for a_char in char_not_found[a_player]:
            out_text += "\t{s}\t1".format(s=a_char)
        out_text += "\n"
    # Print information to screen or to file
    if char_not_found != {} or player_not_found != {}:
        print(out_text)
    # Return
    return return_list


def main(argv):
    event = 'Quarantainment'
    input_file = ''
    try:
        opts, args = getopt.getopt(argv, "he", ["event="])
    except getopt.GetoptError:
        print('create_top8_graphic.py -e <event>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('create_top8_graphic.py -e <event>')
            sys.exit()
        elif opt in ("-e", "--event"):
            event = arg
    # End of Command Line Arguments

    # 0. Setup information
    # Event
    global _properties
    _properties = setGlobalsTop8(event)
    # Read Player Database and Character Database
    global _character_database
    _character_database = populate_globals.readCharDatabase('Character_Database.csv', )
    global _player_database
    _player_database = populate_globals.readPlayerDatabase('Player_Database.csv', char_database=_character_database)
    # 1. Read in the input file to get event info and player placements
    event_info, event_placements = readGrpahicLines(_properties['top8_info'])
    # Update placements and grab character renders
    event_placements = createPlacements(event_placements)
    # Setup
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
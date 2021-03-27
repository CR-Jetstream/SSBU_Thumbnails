"""
Script to create thumbnails for YouTube for Smash Ultimate

1. Read in the names file to get event, round, names, characters information

2. Have a blank graphic ready to populate the information

3. Have the script read in the character and add them to the graphic

4. Have the script open the graphic and add the information

7. Have the script output the images in a specified File location
"""

import io
import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from populate_globals import *

import sys
import getopt

'''Global Variables used in script'''
# Dictionaries for lookups
_character_database = {}
_player_database = {}
# Dictionary for global properties
_properties = dict()


class Match:
    def __init__(self, _title, _event, _round, _player1, _char1, _player2, _char2):
        self.t = _title
        self.e = _event
        self.r = _round
        self.p1 = _player1
        self.c1 = _char1
        self.c1_renders = []
        self.p2 = _player2
        self.c2 = _char2
        self.c2_renders = []
        self.Images = []


def common_start(sa, sb):
    """
    returns the longest common substring from the beginning of sa and sb
    :param sa:
    :param sb:
    :return:
    """

    def _iter():
        for a, b in zip(sa, sb):
            if a == b:
                yield a
            else:
                return

    return ''.join(_iter())


def create_rotated_text(angle, text, font):
    """
    Creates angled text and returns a mask of the text
    :param angle:
    :param text:
    :param font:
    :return:
    """
    # get the size of the text
    x_text, _ = font.getsize(text)
    _, y_text = font.getsize("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz[]")
    # want the tallest possible word

    # build a transparency mask large enough to hold the text
    max_dim = 2 * max(x_text, y_text)

    # build a transparency mask large enough to hold the text
    mask_size = (max_dim, max_dim)
    mask = Image.new('L', mask_size, 0)

    # add text to mask at center of box
    draw = ImageDraw.Draw(mask)
    draw.text((max_dim / 2 - x_text / 2, max_dim / 2 - y_text / 2), text, 255, font=font)

    if angle % 90 == 0:
        # rotate by multiple of 90 deg is easier
        rotated_mask = mask.rotate(angle)
    else:
        # rotate an an enlarged mask to minimize jaggies
        bigger_mask = mask.resize((max_dim * 8, max_dim * 8), resample=Image.BICUBIC)
        rotated_mask = bigger_mask.rotate(angle).resize(mask_size, resample=Image.LANCZOS)

    # return text transparency mask
    return rotated_mask


def hex_to_rgb(hex_input):
    """
    converts a single hex input into RGB tuple
    :param hex_input:
    :return:
    """
    hex_input = hex_input.lstrip('#')
    hlen = len(hex_input)
    return tuple(int(hex_input[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))


def setGlobals(weekly, number, property_settings=None):
    """
    Set all globals based off the type of event. Weekly is the series, Number is the event number.
    These globals are set to then create the associated thumbnails
    :param weekly:
    :param number:
    :param property_settings:
    :return:
    """
    # Set globals based off of type of weekly
    if weekly == 'Quarantainment':
        global_properties = populate_globals.setGlobalsQuarantainment(number)
    elif weekly == 'Students x Treehouse':
        global_properties = populate_globals.setGlobalsSxT(number)
    elif weekly == 'Fro Fridays':
        global_properties = populate_globals.setGlobalsFro(number)
    elif weekly == 'AWG':
        global_properties = populate_globals.setGlobalsAWG(number)
    elif weekly == 'C2C Finale':
        global_properties = populate_globals.setGlobalsC2C(number)
    else:
        global_properties = populate_globals.set_default_properties()
    # return properties
    return global_properties


def readMatchLines(filename):
    """
    Open file and read in line by line
    return a list of lines with match information
    :param filename:
    :return:
    """
    # Open File
    file = io.open(filename, "r", encoding='utf8')
    file_text = file.readlines()
    # Filter through lines that matter:
    return_lines = []
    for line in file_text:
        # check for format
        # {event_1} {round_1} - {player_1} ({char_1}) Vs {player_2} ({char_2}) - SSBU
        if line.startswith('#'):
            # Comment case
            continue
        elif ' - ' in line and '(' in line and ')' in line and '- SSBU' in line:
            if 'Vs' in line or 'vs' in line:  # 'vs' is flexible
                return_lines.append(line)
    # end loop
    if len(return_lines) == 0:
        raise NameError("Filename " + filename + " was not properly read in")
    return return_lines


def createMatches(match_lines, log_file=None):
    """
    Take in list of line information, create a list of matches
    Writes out information to log file if present
    :param match_lines:
    :param log_file:
    :return:
    """
    # Read each line and grab information
    return_list = []
    # Event name is present in every match at the beginning of the line
    #  Use common_start function to compare lines and get the common beginning substring
    # Loop through list - event is the same in the whole list
    event = match_lines[0].strip()
    for a_line in match_lines:
        # set event to starting substring
        event = common_start(a_line, event).strip()
    # dictionaries for players and characters not found
    player_not_found = {}
    char_not_found = {}

    # Read in Match Lines to grab initial match information
    #  {event_1} {round_1} - {player_1} ({char_1}) Vs. {player_2} ({char_2}) - SSBU
    print("--- Reading Match Lines ---")
    match_list = []
    r_start = len(event)  # index for reading the round information
    for a_line in match_lines:
        # grab whole title
        a_title = a_line.strip()
        # trim off the event
        a_line = a_line[r_start:]
        # split based off '-' to grab round information
        a_line = a_line.split(' - ', 1)
        a_round = a_line[0].strip()
        a_line = a_line[1]
        # split based off of Vs. to get Player 1 and Player 2
        if ' Vs ' in a_line:
            a_line = a_line.split(' Vs ', 1)
        elif ' vs ' in a_line:
            a_line = a_line.split(' vs ', 1)
        else:
            NameError("Error in file format, unable to split on 'Vs'")
        player1_info = a_line[0]
        player2_info = a_line[1]
        # Grab player 1 name and characters {player_1} ({char_1})
        player1_info = player1_info.split('(')
        player1_name = player1_info[0].strip()
        player1_chars = player1_info[1]
        player1_chars = player1_chars.split(')')[0]  # trim off ')'
        player1_chars = [x.strip() for x in player1_chars.split(',')]  # create a list for characters
        # Grab player 2 name and characters {player_2} ({char_2})
        player2_info = player2_info.split('(')
        player2_name = player2_info[0].strip()
        player2_chars = player2_info[1]
        player2_chars = player2_chars.split(')')[0]  # trim off ')'
        player2_chars = [x.strip() for x in player2_chars.split(',')]  # create a list for characters (strip whitespace)
        # Have all the information, create a match
        a_match = Match(a_title, event, a_round, player1_name, player1_chars, player2_name, player2_chars)
        match_list.append(a_match)
    # end of match creation

    # Loop through all matches and find character render file locations
    #  This involves looking at the Character and Player Databases to successfully grab the alts
    for a_match in match_list:
        # Loop through character lists and grab character render
        #  Add them to the new lists
        player1_char_files = []
        player2_char_files = []
        p1_flag = True  # used in loop
        for a_list in [a_match.c1, a_match.c2]:
            # Loop through all characters and find their file locations
            for a_char in a_list:
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
                    if p1_flag:
                        player_name = a_match.p1
                    else:
                        player_name = a_match.p2
                    # Remove [L] suffix if present when searching for player
                    if player_name[-4:] == ' [L]':
                        player_name = player_name[:-4]
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
                        raise NameError("Character not found in " + a_match.r + ": " + rend_dir + "/" + char_file)
                # Add to render files
                if p1_flag:
                    player1_char_files.append(char_file)
                else:
                    player2_char_files.append(char_file)
            # end of character loop
            p1_flag = False  # flip boolean
        # end of c1, c2 loop
        # Add character renders to match
        a_match.c1_renders = player1_char_files
        a_match.c2_renders = player2_char_files
        # Add match to return list
        return_list.append(a_match)
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
    if log_file == '':
        print(out_text)
    else:
        out_file = open(log_file, "w")
        out_file.write(out_text)
        out_file.close()
    # Return
    return return_list


def calculateCenter(xy_image):
    """
    Function to calculate the center location of a xy size
    Returns an integer value
    :param xy_image:
    :return:
    """
    x_image, y_image = xy_image
    return int(x_image / 2), int(y_image / 2)


def calculateOffsetFromCenter(xy_center, xy_image):
    """
    Function to calculate the offset needed to fit image at the center of a window
    :param xy_center:
    :param xy_image:
    :return:
    """
    x_center, y_center = xy_center
    x_image, y_image = xy_image
    x_off = int(x_center - (x_image / 2))
    y_off = int(y_center - (y_image / 2))
    return x_off, y_off


def resizeCharacterList(char_list, num_resizes):
    """
    Function to resize the characters in char list for
    Returns a list of images with each resize as an element in the list.
    The order is the same as the char_list
    Num resizes identifies the number of resizes present
    This function will only go up to 3 character resizes
    :param char_list:
    :param num_resizes:
    :return:
    """
    return_list = []
    # Loop through the characters
    for a_char in char_list:
        return_list.append([])
        # Resize are global variables that scale the renders
        for a_resize in [_properties['resize_1'], _properties['resize_2'], _properties['resize_3']]:
            x_resize, y_resize = a_char.size
            x_resize = int(x_resize * a_resize)
            y_resize = int(y_resize * a_resize)
            new_char = a_char.resize((x_resize, y_resize))
            return_list[-1].append(new_char)
            # break if number of characters in list is equal to num_resizes
            if len(return_list[-1]) == num_resizes:
                break
    # end of loop
    return return_list


def createCharacterWindow(char_list, win_size, right_bool=False, single_bool=False, border_bool=True):
    """
    Function to create images of the characters in a single image.
    Returns a list of images with the character models.
    Right bool is to identify this is a Player 2 image and not a Player 1 image.
    Single bool is to decide if there is only one character in the image.
    Border bool is used when there wishes to be padding around the character placement.
        This will pad with respect to win_size
    :param char_list:
    :param win_size:
    :param right_bool:
    :param single_bool:
    :param border_bool:
    :return:
    """
    # Create Canvas
    canvas = Image.new('RGBA', win_size, (255, 0, 0, 0))
    canvas_list = []
    resized_char1 = []
    resized_char2 = []
    resized_char3 = []

    # 1. Resize all the images to fit in this canvas
    # Check border bool to apply a border for canvas
    if not border_bool:
        x_max_height, y_max_height = win_size
    else:
        # apply border
        char_border = _properties['char_border']
        x_max_height = int(win_size[0] * (1 - char_border[0]))
        y_max_height = int(win_size[1] * (1 - char_border[1]))
    # Identify ratio for scaling
    xy_ratio = x_max_height / y_max_height
    # Loop through render types and save the images to resized_char lists
    resized_char_list = [resized_char1, resized_char2, resized_char3]
    render_list = [_properties['render_type'], _properties['render_type2'], _properties['render_type3']]
    for a_render, a_resize in zip(render_list, resized_char_list):
        # Check for None case for render
        if a_render is None:
            # skip remaining loop
            continue
        for a_char in char_list:
            # Open character render
            char_image = Image.open(os.path.join(_properties['char_renders'], a_render, a_char + '.png'))
            # Check if not rgba image
            if char_image.mode != 'RGBA':
                char_image = char_image.convert('RGBA')
            # Cases for different renders
            if a_render == "Full render":
                # Resize the image such that it fits in the window while maintaining its aspect ratio
                x_char, y_char = char_image.size
                if y_char * xy_ratio > x_char:
                    # character image is taller than it is wide
                    scaler_ratio = y_max_height / y_char
                    y_resize = y_max_height  # = ratio*input_y
                    x_resize = scaler_ratio * x_char
                else:
                    # character image is wider than it is tall
                    scaler_ratio = x_max_height / x_char
                    x_resize = x_max_height  # = ratio*input_x
                    y_resize = scaler_ratio * y_char
                # Resize the character image. No need to worry about offsets
                xy_resize = (int(x_resize), int(y_resize))
                char_image = char_image.resize(xy_resize)
            # End of Full render
            # elif a_resize == "Wide render":
            # elif a_resize == "Body render":
            # else: No change
            # Add resized character to list
            a_resize.append(char_image)
        # end of char loop
    # 2. Now take the characters and apply them to the canvas
    # enf of loop
    #  Each offset for each character depends on the number of characters
    #  Create permutations for which character in front
    # Grab center shifts from properties
    center_shift_1 = _properties['center_shift_1']
    center_shift_2_1 = _properties['center_shift_2_1']
    center_shift_2_2 = _properties['center_shift_2_2']
    center_shift_3_1 = _properties['center_shift_3_1']
    center_shift_3_2 = _properties['center_shift_3_2']
    center_shift_3_3 = _properties['center_shift_3_3']
    # Calculate center and offsets
    x_center, y_center = calculateCenter(win_size)
    # Flip sign if on the right of the canvas instead of the left
    x_sign = 1
    if right_bool:
        x_sign = -1
    # This is the center-point offset of the character render
    offset_shift_1 = (x_sign * int(win_size[0] * center_shift_1[0]), int(win_size[1] * center_shift_1[1]))
    # This is the center-point offsets for 2 characters
    offset_shift_2_1 = (int(win_size[0] * center_shift_2_1[0]), int(win_size[1] * center_shift_2_1[1]))
    offset_shift_2_2 = (int(win_size[0] * center_shift_2_2[0]), int(win_size[1] * center_shift_2_2[1]))
    # This is the center-point offset for 3 character
    offset_shift_3_1 = (int(win_size[0] * center_shift_3_1[0]), int(win_size[1] * center_shift_3_1[1]))
    offset_shift_3_2 = (int(win_size[0] * center_shift_3_2[0]), int(win_size[1] * center_shift_3_2[1]))
    offset_shift_3_3 = (int(win_size[0] * center_shift_3_3[0]), int(win_size[1] * center_shift_3_3[1]))
    # Calculate for each character offsets based on character count
    num_chars = len(char_list)
    if num_chars == 1 or single_bool:  # 2.1 One character
        resized_list = [resized_char1]
        # acquire resized characters from scaling
        # TODO: explain this section, maybe adjust globals??
        if single_bool:
            resized_list = resizeCharacterList(resized_char1, 1)
        # apply characters to canvas, add to canvas list
        for a_char in resized_list:
            # set a_char equal to the only element in the list
            a_char = a_char[0]
            a_canvas = canvas.copy()
            # Calculate offset and shift from center
            a_offset = calculateOffsetFromCenter((x_center, y_center), a_char.size)
            a_offset = a_offset[0] + offset_shift_1[0], a_offset[1] + offset_shift_1[1]
            # Paste character
            a_canvas.paste(a_char, a_offset, mask=a_char)
            canvas_list.append(a_canvas)
    elif num_chars == 2:  # 2.2 Two characters
        # acquire resized characters from scaling for multiple characters
        resized_list = resizeCharacterList(resized_char1, 2)
        resized_list2 = resizeCharacterList(resized_char2, 2)
        # check if list 2 is empty
        if resized_char2 == []:
            resized_list2 = resized_list
        # Calculate center for resized images
        a_center = x_center + offset_shift_1[0] + offset_shift_2_1[0], y_center + offset_shift_1[1] + offset_shift_2_1[1]
        b_center = x_center + offset_shift_1[0] + offset_shift_2_2[0], y_center + offset_shift_1[1] + offset_shift_2_2[1]
        # two character, two permutations on order of characters
        for a_ind in range(0, 2):
            for b_ind in range(0, 2):
                # skip if indices are equal
                if a_ind == b_ind:
                    continue
                a_canvas = canvas.copy()
                # grab sizes of appropriate characters
                a_char = resized_list[a_ind][0]  # This is the first character on the canvas
                b_char = resized_list2[b_ind][1]  # second character on the canvas
                # grab offsets
                a_char_offset = calculateOffsetFromCenter(a_center, a_char.size)
                b_char_offset = calculateOffsetFromCenter(b_center, b_char.size)
                # paste characters
                a_canvas.paste(b_char, b_char_offset, mask=b_char)  # order matters for pasting
                a_canvas.paste(a_char, a_char_offset, mask=a_char)
                canvas_list.append(a_canvas)
                # Canvas1 [Char1, Char2]
                # Canvas2 [Char2, Char1]
        # end of loop
    elif num_chars >= 3:  # 2.3 Three characters (or more, only take first three)
        # acquire resized characters from scaling for multiple characters
        resized_list = resizeCharacterList(resized_char1, 3)
        resized_list2 = resizeCharacterList(resized_char2, 3)
        resized_list3 = resizeCharacterList(resized_char3, 3)
        # check if list 2 and 3 are empty
        if resized_list2 == []:
            resized_list2 = resized_list
        if resized_char3 == []:
            resized_list3 = resized_list2
        # Calculate center for resized images
        a_center = x_center + offset_shift_1[0] + offset_shift_3_1[0], y_center + offset_shift_1[1] + offset_shift_3_1[
            1]
        b_center = x_center + offset_shift_1[0] + offset_shift_3_2[0], y_center + offset_shift_1[1] + offset_shift_3_2[
            1]
        c_center = x_center + offset_shift_1[0] + offset_shift_3_3[0], y_center + offset_shift_1[1] + offset_shift_3_3[
            1]
        # three character, six permutations on order of characters
        for a_ind in range(0, 3):
            for b_ind in range(0, 3):
                for c_ind in range(0, 3):
                    # skip if indices are equal
                    if a_ind == b_ind or a_ind == c_ind or b_ind == c_ind:
                        continue
                    a_canvas = canvas.copy()
                    # grab sizes of appropriate characters
                    a_char = resized_list[a_ind][0]  # This is the first character on the canvas
                    b_char = resized_list2[b_ind][1]  # second character on the canvas
                    c_char = resized_list3[c_ind][2]  # third character on the canvas
                    # grab offsets
                    a_char_offset = calculateOffsetFromCenter(a_center, a_char.size)
                    b_char_offset = calculateOffsetFromCenter(b_center, b_char.size)
                    c_char_offset = calculateOffsetFromCenter(c_center, c_char.size)
                    # past characters
                    a_canvas.paste(c_char, c_char_offset, mask=c_char)  # order matters for pasting
                    a_canvas.paste(b_char, b_char_offset, mask=b_char)
                    a_canvas.paste(a_char, a_char_offset, mask=a_char)
                    canvas_list.append(a_canvas)
                    # Canvas1 [Char1, Char2, Char3]
                    # Canvas2 [Char1, Char3, Char2]
                    # Canvas3 [Char2, Char1, Char3]
                    # Canvas4 [Char2, Char3, Char1]
                    # Canvas5 [Char3, Char1, Char2]
                    # Canvas6 [Char3, Char2, Char1]
        # end of loop

    # Return canvas list
    return canvas_list


def createRoundImages(match_list, background, foreground):
    """
    Creates images based off of the content in match list and applies it to the Background and Foreground images
    :param match_list:
    :param background:
    :param foreground:
    :return:
    """
    # Loop through the matches and add the images
    print("--- Creating Match Images ---")
    show_first = _properties['show_first_image']
    for a_match in match_list:
        # # # Create background and foreground images and combine
        # # Background:
        # Grab all the character images to prepare them to add to the background
        c1_char_list = a_match.c1_renders
        c2_char_list = a_match.c2_renders
        # Call Function to create the combined character images - Left and Right space
        char_window = _properties['char_window']
        one_char_flag = _properties['one_char_flag']
        char_canvas = (int(background.size[0] * char_window[0]), int(background.size[1] * char_window[1]))
        c1_image_list = createCharacterWindow(c1_char_list, char_canvas, single_bool=one_char_flag)
        c2_image_list = createCharacterWindow(c2_char_list, char_canvas, right_bool=True, single_bool=one_char_flag)
        # Grab offsets for placing the character windows
        char_offset1 = _properties['char_offset1']
        offset1 = (int(background.size[0] * char_offset1[0]), int(background.size[1] * char_offset1[1]))
        char_offset2 = _properties['char_offset2']
        offset2 = (int(background.size[0] * char_offset2[0]), int(background.size[1] * char_offset2[1]))
        # Add characters to background, create every permutation and insert into Match.Images
        #  Add filter for pixelation if true
        for c1_image in c1_image_list:
            for c2_image in c2_image_list:
                # Add characters to canvas
                if not _properties['char_glow_bool']:
                    # Paste character models to transparent canvas
                    blank_back = Image.new("RGBA", background.size)
                    blank_back.paste(c1_image, offset1, mask=c1_image)
                    blank_back.paste(c2_image, offset2, mask=c2_image)
                    # Make new composite image of background and characters
                    match_back = Image.alpha_composite(background.copy(), blank_back)
                else:  # apply with transparency glow
                    # Create a copy of the background
                    match_back = background.copy()
                    # Apply the characters to the image
                    match_back.paste(c1_image, offset1, mask=c1_image)
                    match_back.paste(c2_image, offset2, mask=c2_image)
                # Pixelate if filter is set
                if _properties['pixelate_filter_bool']:
                    # Resize smoothly down to x pixels
                    pixel_size = _properties['pixelate_filter_size']
                    temp_image = match_back.resize((pixel_size, pixel_size), resample=Image.BILINEAR)
                    # Scale back up using NEAREST to original size
                    match_back = temp_image.resize(match_back.size, Image.NEAREST)
                # End of pixelate
                # Add this image to Match.Images
                a_match.Images.append(match_back)
        # # Foreground:
        # Take match information and populate the foreground
        # Apply this foreground to all the images in Match.Images list
        match_fore = foreground.copy()
        # Apply the Text information to the desired locations on the foreground
        # Grab Font information
        # TODO: open font as part of the set globals function so the imagefont is not called every loop
        font_player1 = ImageFont.truetype(_properties['font_location'], size=_properties['font_player1_size'])
        font_player2 = ImageFont.truetype(_properties['font_location'], size=_properties['font_player2_size'])
        font_event = ImageFont.truetype(_properties['font_location'], size=_properties['font_event_size'])
        font_round = ImageFont.truetype(_properties['font_location'], size=_properties['font_round_size'])
        # Loop through the following [ Player 1, Player 2, Event, Round ]
        font_list = [font_player1, font_player2]
        text_center_list = [_properties['text_player1'], _properties['text_player2']]
        text_contents = [a_match.p1, a_match.p2]
        text_colors = [_properties['font_color1'], _properties['font_color2']]
        # Case for combining Event and Round - [ Player 1, Player 2, Event&Round]
        if _properties['event_round_single_text']:
            font_list.append(font_event)
            text_center_list.append(_properties['text_event'])
            text_contents.append(a_match.e + _properties['event_round_text_split'] + a_match.r)
            text_colors.append(_properties['font_color3'])
        else:  # Normal case
            font_list.extend([font_event, font_round])
            text_center_list.extend([_properties['text_event'], _properties['text_round']])
            text_contents.extend([a_match.e, a_match.r])
            text_colors.extend([_properties['font_color3'], _properties['font_color4']])
        # Apply text on foreground image
        for t_font, t_center, t_contents, t_color in zip(font_list, text_center_list, text_contents, text_colors):
            # Determine center point for text
            t_offset = (int(foreground.size[0] * t_center[0]), int(foreground.size[1] * t_center[1]))
            t_mask = create_rotated_text(_properties['text_angle'], t_contents, t_font)
            # apply mask to image at location
            color_image = Image.new('RGBA', t_mask.size, color=t_color)
            # apply shadow if present
            if _properties['font_glow_bool']:
                # Blur the mask by applying a filter
                t_shadow_size = t_mask.size
                filter_image = Image.new('RGBA', t_shadow_size, color=_properties['font_glow_color'])
                t_filter = t_mask.filter(ImageFilter.BoxBlur(_properties['font_glow_px']))
                # Calculate offset for filter
                font_filter_offset = _properties['font_glow_offset']
                t_filter_offset = (t_offset[0] + font_filter_offset[0], t_offset[1] + font_filter_offset[1])
                # Apply filter to image
                for i in range(0, _properties['font_glow_itr']):
                    match_fore.paste(filter_image, calculateOffsetFromCenter(t_filter_offset, t_filter.size),
                                     mask=t_filter)
            # Apply text to image
            match_fore.paste(color_image, calculateOffsetFromCenter(t_offset, t_mask.size), mask=t_mask)
        # # Combine
        # Loop through Match.Images and create composite image of the background and foreground
        background_ims = a_match.Images
        a_match.Images = []
        for an_image in background_ims:
            # Make new composite image of Background and Foreground
            comb_image = Image.alpha_composite(an_image, match_fore)
            a_match.Images.append(comb_image)
            # Show image
            if show_first:
                comb_image.show()
                show_first = False
                # return match_list
        # end of inner loop
        print("Image:", a_match.t)
    # end loop
    return match_list


def saveImages(match_list, folder_location, event_bool=False):
    """
    Saves images to folder location. If event name is true, then create a folder with the event name
    :param match_list:
    :param folder_location:
    :param event_bool:
    :return:
    """
    # Check if event is being used as folder name
    if event_bool is True:
        event_name = match_list[0].e
        folder_location = os.path.join(folder_location, event_name)
    # Create folder if it does not exist
    if not os.path.exists(folder_location):
        os.makedirs(folder_location)
    # Save images with the following style #.## {match_name}
    #  Matches are ordered, with # as that number
    #  The second number ## is to distinguish different thumbnails with characters swapped around
    count_1 = 1
    for a_match in match_list:
        count_2 = 1
        for an_image in a_match.Images:
            an_image.save(os.path.join(folder_location, str(count_1) + '.' + str(count_2) + ' ' + a_match.t + '.png'))
            an_image.close()
            count_2 += 1
        count_1 += 1
    return


def main(argv):
    event = 'Sample'
    number = 'Test'
    property_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "he:n:p:o:", ["event=", "number=", "property_file=", "output_file="])
    except getopt.GetoptError:
        print('create_thumbnail.py -e <event> -n <number>, -p <property_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('create_thumbnail.py -e <event> -n <number>, -p <property_file> -o <output_file>')
            sys.exit()
        elif opt in ("-e", "--event"):
            event = arg
        elif opt in ("-n", "--number"):
            number = arg
        elif opt in ("-p", "--property_file"):
            property_file = arg
        elif opt in ("-o", "--output_file"):
            output_file = arg
    print('Event is', event, number)
    # print('Property file is ', property_file)
    # End of Command Line Arguments

    # 0. Setup information
    # Event
    global _properties
    _properties = setGlobals(event, number, property_file)
    # setGlobals('Sample', 'test')
    # setGlobals('Quarantainment', '43')
    # setGlobals('Students x Treehouse', '8')
    # setGlobals('Fro Friday', 'test')
    # setGlobals('AWG', 'test')
    # Read Player Database and Character Database
    global _character_database
    _character_database = populate_globals.readCharDatabase('Character_Database.csv', )
    global _player_database
    _player_database = populate_globals.readPlayerDatabase('Player_Database.csv', char_database=_character_database)
    # 1. Read in the names file to get event, round, names, characters information
    event_match_lines = readMatchLines(_properties['event_info'])
    # match_lines = readMatchLines('..\\Vod Names\\Students x Treehouse 8 names.txt')
    # create list of matches
    event_match_list = createMatches(event_match_lines, output_file)
    # 2. Have a blank graphic ready to populate the information
    back_image = Image.open(_properties['background_file'])
    # back_image = Image.open('Overlays\\Background_U32.png')
    # back_image.show()
    # front_image = Image.open('Overlays\\Foreground_U32.png')
    front_image = Image.open(_properties['foreground_file'])
    # front_image = Image.open('Overlays\\Foreground_Roth.png')
    # front_image = Image.open('Overlays\\Foreground_SxT.png')
    # front_image.show()
    # 3. Have the script read in the character and add them to the graphic
    event_match_list = createRoundImages(event_match_list, back_image, front_image)
    # 4. Save the images
    saveImages(event_match_list, _properties['save_location'], event_bool=True)


if __name__ == "__main__":
    # Get command line inputs
    main(sys.argv[1:])
    print("Done")

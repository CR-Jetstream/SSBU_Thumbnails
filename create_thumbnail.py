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
import populate_globals

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
        self.p2 = _player2
        self.c2 = _char2
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


def readCharDatabase(filename, deliminator=','):
    """
    Open and read player database from a file.
    By default, it is expected to be a CSV format
    Line: Player,character,alt,character,alt,character,alt,character,alt, ...
    Populate the Player Database dictionary for use
    :param filename:
    :param deliminator:
    :return:
    """
    # Open File
    file = io.open(filename, "r", encoding='utf8')
    file_text = file.readlines()
    # Filter through lines that matter:
    global _character_database
    for line in file_text:
        # check for format
        if line.startswith('#'):
            continue  # comment line
        # {Char from names},{Char in filename}
        line = line.split(deliminator)
        if len(line) < 2:
            continue
        # Confirm there are two columns
        if len(line) > 2:
            print("Warning: Bad format in player database", line)
            continue
        # grab character name
        char_key = line.pop(0).strip()
        char_value = line.pop(0).strip()
        # Add to character database dictionary (change to upper case)
        _character_database[char_key] = char_value.upper()
    # end loop
    return


def readPlayerDatabase(filename, deliminator=','):
    """
    Open and read player database from a file.
    By default, it is expected to be a CSV format
    Line: Player,character,alt,character,alt,character,alt,character,alt, ...
    Populate the Player Database dictionary for use
    :param filename:
    :param deliminator:
    :return:
    """
    # Open File
    file = io.open(filename, "r", encoding='utf8')
    file_text = file.readlines()
    # Filter through lines that matter:
    global _player_database
    for line in file_text:
        # check for format
        if line.startswith('#'):
            continue  # comment line
        # {player},{Char_1},{Alt_1},{Char_2},{Alt_2},{Char_3},{Alt_3}, ...
        line = line.split(deliminator)
        # check if at least one char alt combination exists
        if len(line) < 3:
            continue
        # check for odd count (requesting char & alt combinations)
        if len(line) % 2 == 0:
            print("Warning: Bad format in player database", line)
            continue
        # grab player name
        player_name = line.pop(0)
        # loop through character & alts
        char_alt_list = []
        for i in range(0, len(line), 2):
            j = i + 1
            a_char = line[i].strip()
            a_alt = line[j].strip()
            # skip if blank
            if a_char == '' and a_alt == '':
                continue
            # check character mapping
            if a_char in _character_database.keys():
                a_char = _character_database[a_char]
            # format "{character} ({alt})"
            a_char_alt = '{char} ({alt})'.format(char=a_char, alt=a_alt)
            # Confirm character image exists
            if not os.path.exists(os.path.join(_properties['char_renders'], a_char_alt + '.png')):
                raise NameError("Character and alt not found in player database: " + a_char_alt)
            # add char alt combo to list
            char_alt_list.append(a_char_alt)
        # Add to player database dictionary
        _player_database[player_name] = char_alt_list
    # end loop
    return


def setGlobals(weekly, number, property_settings):
    """
    Set all globals based off the type of event. Weekly is the series, Number is the event number.
    These globals are set to then create the associated thumbnails
    :param weekly:
    :param number:
    :return:
    """
    # Set properties to default
    global _properties
    _properties = populate_globals.set_default_properties()
    # Modify globals based off of type of weekly
    if weekly == 'Quarantainment':
        setGlobalsQuarantainment(number)
    elif weekly == 'Students x Treehouse':
        setGlobalsSxT(number)
    elif weekly == 'Fro Fridays':
        setGlobalsFro(number)
    elif weekly == 'AWG':
        setGlobalsAWG(number)


def setGlobalsQuarantainment(number):
    """
    Set necessary globals for Quarantainment event {number}
    :param number:
    :return:
    """
    global _properties
    # Event match file information location
    _properties['event_info'] = os.path.join('..', 'Vod Names', 'Quarantainment {s} names.txt'.format(s=number))
    # Foreground overlay locations
    _properties['foreground_file'] = os.path.join('Overlays', 'Foreground_Q.png')


def setGlobalsSxT(number):
    """
    Set necessary globals for Students x Treehouse event {number}
    :param number:
    :return:
    """
    global _properties
    # Event match file information location
    _properties['event_info'] = os.path.join('..', 'Vod Names', 'Students x Treehouse {s} names.txt'.format(s=number))
    # Foreground overlay locations
    _properties['foreground_file'] = os.path.join('Overlays', 'Foreground_SxT.png')


def setGlobalsFro(number):
    """
    Set all globals for Fro Friday event {number}
    :param number:
    :return:
    """
    global _properties
    # Event match file information location
    _properties['event_info'] = os.path.join('..', 'Vod Names', 'Fro Fridays {s} names.txt'.format(s=number))
    # Background and Foreground overlay locations
    _properties['background_file'] = os.path.join('Overlays', 'Background_Fro.png')
    _properties['foreground_file'] = os.path.join('Overlays', 'Foreground_Fro.png')
    # Single character flag on overlay
    _properties['one_char_flag'] = True
    # Center-point shift for canvas for characters
    _properties['center_shift_1'] = (-0.00, +0.00)  # Universal character shift
    # Center-point for text on canvas with respect to whole canvas
    _properties['text_player1'] = (0.20, 0.75)
    _properties['text_player2'] = (0.80, 0.75)
    _properties['text_event'] = (0.50, 0.075)
    _properties['text_round'] = (0.50, 0.075)
    _properties['text_angle'] = 0  # degree of rotation counter-clockwise
    # Font settings
    _properties['font_location'] = os.path.join("Fonts", "LostLeonestReguler-MVVMn.otf")
    _properties['font_player1_size'] = 42
    _properties['font_player2_size'] = 42
    _properties['font_event_size'] = 37
    _properties['font_round_size'] = 37
    _properties['font_glow_bool'] = True
    _properties['font_glow_color'] = '#641fbf'  # (100, 31, 191)
    _properties['font_glow_px'] = 2  # Pixel count for the blur in all directions
    _properties['font_glow_itr'] = 25  # Iterations on applying filter
    _properties['font_glow_offset'] = (0, 2)  # Offset to apply the filtered effect
    # Combined event and round text
    _properties['event_round_single_text'] = True
    _properties['event_round_text_split'] = ' - '


def setGlobalsAWG(number):
    """
    Set all globals for AWG event {number}
    :param number:
    :return:
    """
    global _properties
    # Event match file information location
    _properties['event_info'] = os.path.join('..', 'Vod Names', 'AWG {s} names.txt'.format(s=number))
    # Background and Foreground overlay locations
    _properties['background_file'] = os.path.join('Overlays', 'Background_AWG.png')
    _properties['foreground_file'] = os.path.join('Overlays', 'Foreground_AWG.png')
    # Character border settings
    _properties['char_border'] = (0.00, 0.35)  # border for characters
    _properties['char_offset1'] = (0, -0.00)  # offset for left player window placement on canvas
    _properties['char_offset2'] = (0.5, -0.00)  # offset for right player window placement on canvas
    # Single character flag on overlay
    _properties['one_char_flag'] = True
    # Center-point shift for canvas for characters
    _properties['center_shift_1'] = (+0.03, -0.03)  # Universal character shift
    # Center-point for text on canvas with respect to whole canvas
    _properties['text_player1'] = (0.25, 0.70)
    _properties['text_player2'] = (0.70, 0.70)
    _properties['text_event'] = (0.50, 0.10)
    _properties['text_round'] = (0.50, 0.10)
    _properties['text_angle'] = 0  # degree of rotation counter-clockwise
    # Font settings
    _properties['font_location'] = os.path.join("Fonts", "ConnectionIi-2wj8.otf")
    _properties['font_player1_size'] = 42
    _properties['font_player2_size'] = 42
    _properties['font_event_size'] = 42
    _properties['font_round_size'] = 42
    _properties['font_glow_bool'] = True
    _properties['font_filter_px'] = 2  # Pixel count for the blur in all directions
    _properties['font_filter_itr'] = 15  # Iterations on applying filter
    _properties['font_filter_offset'] = (0, 1)  # Offset to apply the filtered effect
    # Character Pixelation filter to characters
    _properties['pixelate_filter_bool'] = True  # Flag to pixelate the characters
    _properties['pixelate_filter_size'] = 280  # size of pixel squares
    # Combined event and round text
    _properties['event_round_single_text'] = True
    _properties['event_round_text_split'] = ' - '


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
        # {event_1} {round_1} - {player_1} ({char_1}) Vs. {player_2} ({char_2}) Smash Ultimate - SSBU
        if ' - ' in line and '(' in line and ')' in line and 'Vs.' in line and '- SSBU' in line:
            return_lines.append(line)
        elif ' - ' in line and '(' in line and ')' in line and 'vs.' in line and '- SSBU' in line:
            return_lines.append(line)
    # end loop
    if len(return_lines) == 0:
        raise NameError("Filename " + filename + " was not properly read in")
    return return_lines


def createMatches(match_lines):
    """
    Take in list of line information, create a list of matches
    :param match_lines:
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
    # Loop through and grab match data
    #  {event_1} {round_1} - {player_1} ({char_1}) Vs. {player_2} ({char_2}) Smash Ultimate - SSBU
    r_start = len(event)
    for a_line in match_lines:
        # grab whole title
        a_title = a_line.strip()
        # trim off the event
        a_line = a_line[r_start:]
        # split based off '-' to grab round information
        a_line = a_line.split('-', 1)
        a_round = a_line[0].strip()
        a_line = a_line[1]
        # split based off of Vs. to get Player 1 and Player 2
        if 'Vs.' in a_line:
            a_line = a_line.split('Vs.', 1)
        elif 'vs.' in a_line:
            a_line = a_line.split('vs.', 1)
        else:
            NameError("Error in file format, unable to split on Vs.")
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
        # Loop through character lists and grab character render
        #  Add them to the new lists
        player1_char_renders = []
        player2_char_renders = []
        p1_flag = True  # used in loop
        for a_list in [player1_chars, player2_chars]:
            for a_char in a_list:
                # Character lookup in mapping
                if a_char in _character_database.keys():
                    a_char = _character_database[a_char]
                # Presume Character alt 1
                char_file = a_char + ' (1)'
                # Lookup character in player database for alt costume (if it exists)
                if p1_flag:
                    player_name = player1_name
                else:
                    player_name = player2_name
                # Remove [L] suffix if present when searching for player
                if player_name[-4:] == ' [L]':
                    player_name = player_name[:-4]
                # Player not found case
                if player_name not in _player_database.keys():
                    print("-- Note: Player", player_name, "not found in Player Database --")
                else:  # Player found
                    player_chars_lookup = _player_database[player_name]
                    char_found = False
                    for p_char in player_chars_lookup:
                        if a_char.upper() in p_char.upper():
                            char_file = p_char
                            char_found = True
                            break
                    # Char not found case
                    if not char_found:
                        print("-- Note:", a_char, "not found for Player", player_name, "in Player Database --")
                # Check if char file exists
                if not os.path.exists(os.path.join(_properties['char_renders'], char_file + '.png')):
                    raise NameError("Character not found in " + a_round + ": " + char_file)
                # Open character render
                char_image = Image.open(os.path.join(_properties['char_renders'], char_file + '.png'))
                # Check if not rgba image
                if char_image.mode != 'RGBA':
                    char_image = char_image.convert('RGBA')
                # Add to renders
                if p1_flag:
                    player1_char_renders.append(char_image)
                else:
                    player2_char_renders.append(char_image)
            # end of loop
            p1_flag = False  # flip boolean
        # end of loop

        # Have all the information, create a match
        a_match = Match(a_title, event, a_round, player1_name, player1_char_renders, player2_name, player2_char_renders)
        return_list.append(a_match)
    # end of loop
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
    resized_char = []
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
    for a_char in char_list:
        x_char, y_char = a_char.size
        # Resize the image such that it fits in the window while maintaining its aspect ratio
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
        # Add resized character to list
        resized_char.append(a_char.resize(xy_resize))

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
        # apply characters to canvas, add to canvas list
        for a_char in resized_char:
            a_canvas = canvas.copy()
            # Calculate offset and shift from center
            a_offset = calculateOffsetFromCenter((x_center, y_center), a_char.size)
            a_offset = a_offset[0] + offset_shift_1[0], a_offset[1] + offset_shift_1[1]
            # Paste character
            a_canvas.paste(a_char, a_offset, mask=a_char)
            canvas_list.append(a_canvas)
    elif num_chars == 2:  # 2.2 Two characters
        # acquire resized characters from scaling for multiple characters
        resized_list = resizeCharacterList(resized_char, 2)
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
                b_char = resized_list[b_ind][1]  # second character on the canvas
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
        resized_list = resizeCharacterList(resized_char, 3)
        # Calculate center for resized images
        a_center = x_center + offset_shift_1[0] + offset_shift_3_1[0], y_center + offset_shift_1[1] + offset_shift_3_1[
            1]
        b_center = x_center + offset_shift_1[0] + offset_shift_3_2[0], y_center + offset_shift_1[1] + offset_shift_3_2[
            1]
        c_center = x_center + offset_shift_1[0] + offset_shift_3_3[0], y_center + offset_shift_1[1] + offset_shift_3_3[
            1]
        # two character, two permutations on order of characters
        for a_ind in range(0, 3):
            for b_ind in range(0, 3):
                for c_ind in range(0, 3):
                    # skip if indices are equal
                    if a_ind == b_ind or a_ind == c_ind or b_ind == c_ind:
                        continue
                    a_canvas = canvas.copy()
                    # grab sizes of appropriate characters
                    a_char = resized_list[a_ind][0]  # This is the first character on the canvas
                    b_char = resized_list[b_ind][1]  # second character on the canvas
                    c_char = resized_list[c_ind][2]  # third character on the canvas
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
    show_first = _properties['show_first_image']
    for a_match in match_list:
        # # # Create background and foreground images and combine
        # # Background:
        # Grab all the character images to prepare them to add to the background
        c1_renders = a_match.c1
        c2_renders = a_match.c2
        # Call Function to create the combined character images - Left and Right space
        char_window = _properties['char_window']
        one_char_flag = _properties['one_char_flag']
        char_canvas = (int(background.size[0] * char_window[0]), int(background.size[1] * char_window[1]))
        c1_image_list = createCharacterWindow(c1_renders, char_canvas, single_bool=one_char_flag)
        c2_image_list = createCharacterWindow(c2_renders, char_canvas, right_bool=True, single_bool=one_char_flag)
        # Grab offsets for placing the character windows
        char_offset1 = _properties['char_offset1']
        offset1 = (int(background.size[0] * char_offset1[0]), int(background.size[1] * char_offset1[1]))
        char_offset2 = _properties['char_offset2']
        offset2 = (int(background.size[0] * char_offset2[0]), int(background.size[1] * char_offset2[1]))
        # Add characters to background, create every permutation and insert into Match.Images
        #  Add filter for pixelation if true
        for c1_image in c1_image_list:
            for c2_image in c2_image_list:
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
            # Make new composite image, apply Background, then Forground
            comb_image = Image.new("RGBA", an_image.size)
            comb_image = Image.alpha_composite(comb_image, an_image)
            comb_image = Image.alpha_composite(comb_image, match_fore)
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
    try:
        opts, args = getopt.getopt(argv, "he:n:p:", ["event=", "number=", "property_file="])
    except getopt.GetoptError:
        print('create_thumbnail.py -e <event> -n <number>, -p <property_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('create_thumbnail.py -e <event> -n <number>, -p <property_file>')
            sys.exit()
        elif opt in ("-e", "--event"):
            event = arg
        elif opt in ("-n", "--number"):
            number = arg
        elif opt in ("-p", "--property_file"):
            property_file = arg
    print('Event is', event, number)
    # print('Property file is ', property_file)
    # End of Command Line Arguments

    # 0. Setup information
    # Event
    setGlobals(event, number, property_file)
    # setGlobals('Sample', 'test')
    # setGlobals('Quarantainment', '43')
    # setGlobals('Students x Treehouse', '8')
    # setGlobals('Fro Friday', 'test')
    # setGlobals('AWG', 'test')
    # Read Player Database and Character Database
    readCharDatabase('Character_Database.csv')
    readPlayerDatabase('Player_Database.csv')
    # 1. Read in the names file to get event, round, names, characters information
    event_match_lines = readMatchLines(_properties['event_info'])
    # match_lines = readMatchLines('..\\Vod Names\\Students x Treehouse 8 names.txt')
    # create list of matches
    event_match_list = createMatches(event_match_lines)
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

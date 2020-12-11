'''
1. Read in the names file to get event, round, names, characters information

2. Have a blank graphic ready to populate the information

3. Have the script read in the character and add them to the graphic

4. Have the script open the graphic and add the information

7. Have the script output the images in a specified File location
'''

import io
import os
from PIL import Image, ImageDraw, ImageFont
import math

'''Global Variables used in script'''
_character_database = {}
#     # Character : Image
#     'Banjo': 'Banjo and Kazooie',
#     'Cpt Falcon': 'Captain Falcon',
#     'Diddy': 'Diddy Kong',
#     'Game&Watch': 'Mr. Game and Watch',
#     'Game & Watch': 'Mr. Game and Watch',
#     'Ganon': 'Ganondorf',
#     'K. Rool': 'King K. Rool',
#     'King K Rool': 'King K. Rool',
#     'King DDD': 'King DeDeDe',
#     'MegaMan': 'Mega Man',
#     'Mii SwordFighter': 'Mii Swordman',
#     'Pac Man': 'Pac-Man',
#     'PKM Trainer': 'Pokemon Trainer',
#     'ZSS': 'Zero Suit Samus'
#
# }

_player_database = {}


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
    """ returns the longest common substring from the beginning of sa and sb """
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
    _, y_text = font.getsize("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz[]")  # want the tallest possible word

    # build a transparency mask large enough to hold the text
    max_dim = 2*max(x_text, y_text)

    # build a transparency mask large enough to hold the text
    mask_size = (max_dim, max_dim)
    mask = Image.new('L', mask_size, 0)

    # add text to mask at center of box
    draw = ImageDraw.Draw(mask)
    draw.text((max_dim/2 - x_text/2, max_dim/2 - y_text/2), text, 255, font=font)

    if angle % 90 == 0:
        # rotate by multiple of 90 deg is easier
        rotated_mask = mask.rotate(angle)
    else:
        # rotate an an enlarged mask to minimize jaggies
        bigger_mask = mask.resize((max_dim*8, max_dim*8), resample=Image.BICUBIC)
        rotated_mask = bigger_mask.rotate(angle).resize(mask_size, resample=Image.LANCZOS)

    # return text transparency mask
    return rotated_mask


def readCharDatabase(filename, deliminator=','):
    '''
    Open and read player database from a file.
    By default, it is expected to be a CSV format
    Line: Player,character,alt,character,alt,character,alt,character,alt, ...
    Populate the Player Database dictionary for use
    :param filename:
    :param deliminator:
    :return:
    '''
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
        # Add to character database dictionary
        _character_database[char_key] = char_value
    # end loop
    return


def readPlayerDatabase(filename, deliminator=','):
    '''
    Open and read player database from a file.
    By default, it is expected to be a CSV format
    Line: Player,character,alt,character,alt,character,alt,character,alt, ...
    Populate the Player Database dictionary for use
    :param filename:
    :param deliminator:
    :return:
    '''
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
            j = i+1
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
            if not os.path.exists(os.path.join('Character_Renders', a_char_alt + '.png')):
                raise NameError("Character and alt not found in player database: " + a_char_alt)
            # add char alt combo to list
            char_alt_list.append(a_char_alt)
        # Add to player database dictionary
        _player_database[player_name] = char_alt_list
    # end loop
    return


def readMatchLines(filename):
    '''
    Open file and read in line by line
    :param filename:
    :return:
    '''
    # Open File
    file = io.open(filename, "r", encoding='utf8')
    file_text = file.readlines()
    # Filter through lines that matter:
    match_lines = []
    for line in file_text:
        # check for format
        # {event_1} {round_1} - {player_1} ({char_1}) Vs. {player_2} ({char_2}) Smash Ultimate - SSBU
        if ' - ' in line and '(' in line and ')' in line and 'Vs.' in line and '- SSBU' in line:
            match_lines.append(line)
    # end loop
    return match_lines


def createMatches(match_lines):
    '''
    Take in list of line information, create a list of matches
    :param match_list:
    :return:
    '''
    # Read each line and grab information
    match_list = []
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
        a_line = a_line.split('Vs.', 1)
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
        # Loop through character lists and check mapping
        for count in range(0, len(player1_chars)):
            a_char = player1_chars[count]
            if a_char in _character_database.keys():
                player1_chars[count] = _character_database[a_char]
        for count in range(0, len(player2_chars)):
            a_char = player2_chars[count]
            if a_char in _character_database.keys():
                player2_chars[count] = _character_database[a_char]
        # Check that an image exists for their character(s) here
        for a_list in [player1_chars, player2_chars]:
            for a_char in a_list:
                if not os.path.exists(os.path.join('Character_Renders', a_char + ' (1).png')):
                    raise NameError("Character not found in " + a_round+": " + a_char)
        # Have all the information, create a match
        a_match = Match(a_title, event, a_round, player1_name, player1_chars, player2_name, player2_chars)
        match_list.append(a_match)
    # end of loop
    return match_list


def calculateOffset(input_image, background_image, right_bool=False):
    '''
    Calculate the offset and resize information for the input image based off background dimensions
    Desire is to have the image fit nicely in the center of the left or right half of the background
    :param input_image:
    :param background_image:
    :return:
    '''
    back_x, back_y = background_image.size
    input_x, input_y = input_image.size
    # Desire is to have the placement 100 pixels top/bottom boarder (1/7 above/below), and centered on the half
    # x_centerline will be 22% (want that little extra for the middle)
    x_centerline = back_x*0.22
    y_centerline = back_y/2
    x_max_height = back_x/2
    y_max_height = back_y*5/7
    # the window is x_max by y_max. Interested in the limiting dimension
    xy_ratio = x_max_height/y_max_height
    # variables needed for return statement
    x_offset = 0
    y_offset = 0
    x_resize = 0
    y_resize = 0
    # Resize the image based off which dimension is outside the window
    if input_y * xy_ratio > input_x:
        # Image is taller than wide, will center based off x centerline
        # scale image to y_max_height and keep aspect ratio
        ratio = y_max_height/input_y
        y_resize = y_max_height # = ratio*input_y
        x_resize = ratio*input_x
        y_offset = y_centerline - (y_resize/2)
        x_offset = x_centerline - (x_resize/2)
    else:
        # Image is wider than tall, will center based off y centerline
        ratio = x_max_height/input_x
        x_resize = x_max_height # = ratio*input_x
        y_resize = ratio*input_y
        x_offset = x_centerline - (x_resize/2)
        y_offset = y_centerline - (y_resize/2)
    # endif
    if right_bool:
        # flip the offset x coordinate to the other side of the image
        x_offset = back_x - x_centerline - (x_resize/2)
    # Return
    offset = (int(x_offset), int(y_offset))
    resize = (int(x_resize), int(y_resize))
    return offset, resize


def calculateCenter(xy_image):
    """
    Function to calculate the center location of a xy size
    Returns an integer value
    :param xy_image:
    :return:
    """
    x_image, y_image = xy_image
    return int(x_image/2), int(y_image/2)


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


def resizeCraracterList(char_list, num_resizes):
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
    # TODO: these will become global variables
    resize_1 = 0.85
    resize_2 = 0.75
    resize_3 = 0.60
    # Loop through the characters
    for a_char in char_list:
        return_list.append([])
        for a_resize in [resize_1, resize_2, resize_3]:
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


def createCharacterWindow(char_list, win_size, right_bool=False, single_bool=False):
    """
    Function to create images of the characters in a single image.
    Returns a list of images with the character models.
    Right bool is to identify this is a Player 2 image and not a Player 1 image.
    Single bool is to decide if there is only one character in the image.
    :param char_list:
    :param win_size:
    :param right_bool:
    :param single_bool:
    :return:
    """
    # Create Canvas
    # TODO: Create canvas that is larger such that characters do not get cut off
    canvas = Image.new('RGBA', win_size, (255, 0, 0, 0))
    canvas_list = []
    # 1. Resize all the images to fit in this canvas
    resized_char = []
    x_max_height, y_max_height = win_size
    xy_ratio = x_max_height/y_max_height
    for a_char in char_list:
        x_char, y_char = a_char.size
        # Resize the image such that it fits in the window while maintaining its aspect ratio
        if y_char * xy_ratio > x_char:
            # character image is taller than it is wide
            scaler_ratio = y_max_height/y_char
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
    # Calculate center and offsets
    x_center, y_center = calculateCenter(win_size)
    # Flip sign if on the right of the canvas instead of the left
    sign = 1
    if right_bool:
        sign = -1
    # TODO: have offsets as global variables
    # This is the centerline of the characters
    offset_shift = (sign * -int(win_size[0] * 0.04), 0)
    # This is the offsets for 2 characters
    offset_shift_2_1 = (-int(win_size[0] * 0.20), +int(win_size[1] * 0.15))
    offset_shift_2_2 = (+int(win_size[0] * 0.20), -int(win_size[1] * 0.15))
    # This is the shift for a third character
    offset_shift_3_1 = (-int(win_size[0] * 0.15), +int(win_size[1] * 0.20))
    offset_shift_3_2 = (+int(win_size[0] * 0.25), -int(win_size[1] * 0.05))
    offset_shift_3_3 = (-int(win_size[0] * 0.20), -int(win_size[1] * 0.20))
    # Calculate for each character offsets based on character count
    num_chars = len(char_list)
    if num_chars == 1 or single_bool:  # 2.1 One character
        a_offset = calculateOffsetFromCenter(calculateCenter(win_size), resized_char[0].size)
        # shift from center by offset
        a_offset = a_offset[0] + offset_shift[0], a_offset[1] + offset_shift[1]
        # apply characters to canvas, add to canvas list
        for a_char in resized_char:
            a_canvas = canvas.copy()
            a_canvas.paste(a_char, a_offset, mask=a_char)
            canvas_list.append(a_canvas)
    elif num_chars == 2:  # 2.2 Two characters
        # acquire resized characters from scaling for multiple characters
        resized_list = resizeCraracterList(resized_char, 2)
        # Calculate center for resized images
        a_center = x_center + offset_shift[0] + offset_shift_2_1[0], y_center + offset_shift[1] + offset_shift_2_1[1]
        b_center = x_center + offset_shift[0] + offset_shift_2_2[0], y_center + offset_shift[1] + offset_shift_2_2[1]
        # two character, two permutations on order of characters
        for a_ind in range(0, 2):
            for b_ind in range(0, 2):
                # skip if indices are equal
                if a_ind == b_ind:
                    continue
                a_canvas = canvas.copy()
                # grab sizes of appropriate characters
                a_char = resized_list[a_ind][0]  # This is the first character on the canvas
                b_char = resized_list[b_ind][1]             # second character on the canvas
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
        resized_list = resizeCraracterList(resized_char, 3)
        # Calculate center for resized images
        a_center = x_center + offset_shift[0] + offset_shift_3_1[0], y_center + offset_shift[1] + offset_shift_3_1[1]
        b_center = x_center + offset_shift[0] + offset_shift_3_2[0], y_center + offset_shift[1] + offset_shift_3_2[1]
        c_center = x_center + offset_shift[0] + offset_shift_3_3[0], y_center + offset_shift[1] + offset_shift_3_3[1]
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
                    b_char = resized_list[b_ind][1]             # second character on the canvas
                    c_char = resized_list[c_ind][2]              # third character on the canvas
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
    '''
    Creates images based off of the content in match list and applies it to the Background and Foreground images
    :param match_list:
    :param background:
    :param foreground:
    :return:
    '''
    # Loop through the matches and add the images
    show_one = True
    for a_match in match_list:
        # # # Create background and foreground images and combine
        # # Characters:
        # Grab all the character images to prepare them to add to the background
        # TODO: rework this to make all characters present on the window. requires more settings
        # TODO: Insert case for Ike, Bayo, and others with different alts
        c1_renders = []
        # Check player database to character list
        player1 = a_match.p1
        player1 = player1.removesuffix(' [L]')
        player1_chars = []
        if player1 in _player_database.keys():
            player1_chars = _player_database[player1]
        # Open character images for the player
        for char1 in a_match.c1:
            # Override case
            if char1 == 'Blank':
                char1_file = char1 + ' (2)'
            else:
                char1_file = char1 + ' (1)'
            # Check player database for character
            for p1_char in player1_chars:
                if char1 in p1_char:
                    char1_file = p1_char
                    break
            # open character renders
            c1_image = Image.open(os.path.join('Character_Renders', char1_file + '.png'))
            # check if not rgba image
            if c1_image.mode != 'RGBA':
                c1_image = c1_image.convert('RGBA')
            c1_renders.append(c1_image)
        c2_renders = []
        # Check player database to character list
        player2 = a_match.p2
        player2 = player2.removesuffix(' [L]')
        player2_chars = []
        if player2 in _player_database.keys():
            player2_chars = _player_database[player2]
        # Open character images for the player
        for char2 in a_match.c2:
            # Override case
            if char2 == 'Blank':
                char2_file = char2 + ' (2)'
            else:
                char2_file = char2 + ' (1)'
            # Check player database for character
            for p2_char in player2_chars:
                if char2 in p2_char:
                    char2_file = p2_char
                    break
            # open character renders
            c2_image = Image.open(os.path.join('Character_Renders', char2_file + '.png'))
            # check if not rgba image
            if c2_image.mode != 'RGBA':
                c2_image = c1_image.convert('RGBA')
            c2_renders.append(c2_image)
        # # Background:
        # Create images with the characters and add them to the Match.match_Images list
        ## TODO: preset char window and offset locations as global variables
        # Call Function to create the combined character images
        char_window = (int(background.size[0]/2), int(background.size[1]*0.74))
        # Create Left character space
        c1_image_list = createCharacterWindow(c1_renders, char_window)
        offset1 = (0, int(background.size[1]*0.14))
        # Create Right character space
        c2_image_list = createCharacterWindow(c2_renders, char_window, right_bool=True)
        offset2 = (int(background.size[0]/2), int(background.size[1]*0.14))
        # Add characters to background and insert into Match.Images
        for c1_image in c1_image_list:
            for c2_image in c2_image_list:
                # Create a copy of the background
                match_back = background.copy()
                # Apply the characters to the image
                match_back.paste(c1_image, offset1, mask=c1_image)
                match_back.paste(c2_image, offset2, mask=c2_image)
                # Add this image to Match.Images
                a_match.Images.append(match_back)

        # # Foreground
        # Take match information and populate the foreground
        # Apply this foreground to all the images in Match.Images list
        match_fore = foreground.copy()
        # Apply the Text information to the desired locations on the foreground
        font = ImageFont.truetype('C:\\Users\\Jetstream\\AppData\\Local\\Microsoft\\Windows\\Fonts\\tt2004m.ttf', size=45)
        # TODO: Calculate the text offsets and center them
        #calculateTextOffset(a_match, back_image)
        angle = 2
        ## Temporary
        # Player 1
        t_offset = (640-320, 55)
        t_mask = create_rotated_text(angle, a_match.p1, font)
        # apply mask to image at location
        color_image = Image.new('RGBA', t_mask.size, (245, 245, 245))
        match_fore.paste(color_image, calculateOffsetFromCenter(t_offset, t_mask.size), mask=t_mask)
        # Player 2
        t_offset = (640+320, 55)
        t_mask = create_rotated_text(angle, a_match.p2, font)
        # apply mask to image at location
        color_image = Image.new('RGBA', t_mask.size, (245, 245, 245))
        match_fore.paste(color_image, calculateOffsetFromCenter(t_offset, t_mask.size), mask=t_mask)
        # Event
        t_offset = (640-320, 720-55)
        t_mask = create_rotated_text(angle, a_match.e, font)
        # apply mask to image at location
        color_image = Image.new('RGBA', t_mask.size, (245, 245, 245))
        match_fore.paste(color_image, calculateOffsetFromCenter(t_offset,  t_mask.size), mask=t_mask)
        # Round
        t_offset = (640+320, 720-55)
        t_mask = create_rotated_text(angle, a_match.r, font)
        # apply mask to image at location
        color_image = Image.new('RGBA', t_mask.size, (245, 245, 245))
        match_fore.paste(color_image, calculateOffsetFromCenter(t_offset,  t_mask.size), mask=t_mask)
        ##
        # # Combine
        # Loop through Match.Images and apply the foreground
        for an_image in a_match.Images:
            # Apply the Foreground to the Background
            an_image.paste(match_fore, mask=match_fore)
            # Show image
            if show_one:
                an_image.show()
                show_one = False
                #return match_list
        print("Image:", a_match.t)
        # end of inner loop
    # end loop
    return match_list


def saveImages(match_list, folder_location, event_bool=False):
    '''
    Saves images to folder location. If event name is true, then create a folder with the event name
    :param match_list:
    :param folder_location:
    :return:
    '''
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


if __name__ == "__main__":
    # 0. Read Player Database and Character Database
    readCharDatabase('Character_Database.csv')
    readPlayerDatabase('Player_Database.csv')
    # 1. Read in the names file to get event, round, names, characters information
    match_lines = readMatchLines('..\\Vod Names\\Quarantainment 41 names.txt')
    #match_lines = readMatchLines('..\\Vod Names\\Students x Treehouse 8 names.txt')
    # create list of matches
    match_list = createMatches(match_lines)
    # 2. Have a blank graphic ready to populate the information
    back_image = Image.open('Overlays\\Background.png')
    #back_image = Image.open('Overlays\\Background_U32.png')
    # back_image.show()
    #front_image = Image.open('Overlays\\Foreground_U32.png')
    front_image = Image.open('Overlays\\Foreground_Q.png')
    #front_image = Image.open('Overlays\\Foreground_SxT.png')
    # front_image.show()
    # 3. Have the script read in the character and add them to the graphic
    match_list = createRoundImages(match_list, back_image, front_image)
    # 4. Save the images
    save_location = os.path.join('..', 'Youtube_Thumbnails')
    saveImages(match_list, save_location, event_bool=True)

    print("Done")










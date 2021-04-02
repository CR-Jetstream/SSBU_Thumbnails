"""
Script to set globals needed for create_thumbnail
Also populated player and character databases
"""
import io
import os


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
    char_database = {}
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
            print("Warning: Bad format in character database", line)
            continue
        # grab character name
        char_key = line.pop(0).strip()
        char_value = line.pop(0).strip()
        # Add to character database dictionary (to uppercase)
        char_database[char_key.upper()] = char_value
    # end loop
    return char_database


def readPlayerDatabase(filename, deliminator=',', char_database=None):
    """
    Open and read player database from a file.
    By default, it is expected to be a CSV format
    Requires character database to properly look up characters
    Line: Player,character,alt,character,alt,character,alt,character,alt, ...
    Populate the Player Database dictionary for use
    :param filename:
    :param deliminator:
    :param char_database:
    :return:
    """
    # Open File
    if char_database is None:
        char_database = dict()
    file = io.open(filename, "r", encoding='utf8')
    file_text = file.readlines()
    # Filter through lines that matter:
    play_database = {}
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
            # check character mapping (to uppercase)
            if a_char.upper() in char_database.keys():
                a_char = char_database[a_char.upper()]
            # format "{character} ({alt})"
            a_char_alt = '{char} ({alt})'.format(char=a_char, alt=a_alt)
            # add char alt combo to list
            char_alt_list.append(a_char_alt)
        # Add to player database dictionary (to uppercase)
        play_database[player_name.upper()] = char_alt_list
    # end loop
    return play_database


def set_default_properties():
    """
    Function to set default properties for globals needed for create_thumbnail.py
    :return:
    """
    # # Set All property values to a default
    # Dictionary for global properties
    properties = dict()
    # Character renders folder location
    properties['char_renders'] = "Character_Renders"
    properties['render_type'] = "Body render"
    properties['render_type2'] = None
    properties['render_type3'] = None
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'Sample test names.txt')
    # Background and Foreground overlay locations
    properties['background_file'] = os.path.join('Overlays', 'Background Sample.png')
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground Sample.png')
    # Output save location
    properties['save_location'] = os.path.join('..', 'Youtube_Thumbnails')
    # Canvas variables for character window with respect to whole canvas
    properties['char_glow_bool'] = False
    properties['char_window'] = (0.5, 1)  # canvas for characters
    properties['char_border'] = (0.00, 0.00)  # border for characters
    properties['char_offset1'] = (0, 0.00)  # offset for left player window placement on canvas
    properties['char_offset2'] = (0.5, 0.00)  # offset for right player window placement on canvas
    # Scaler Variables for characters in window
    properties['resize_1'] = 1.6  # resize for character for multiple renders on image
    properties['resize_2'] = 1.00
    properties['resize_3'] = 1.00
    # Center-point shift for canvas for characters
    properties['center_shift_1'] = (-0.00, +0.10)  # Universal character shift
    properties['center_shift_2_1'] = (-0.20, +0.11)  # Two character shift
    properties['center_shift_2_2'] = (+0.20, -0.11)
    properties['center_shift_3_1'] = (-0.15, +0.148)  # Three character shift
    properties['center_shift_3_2'] = (+0.25, -0.037)
    properties['center_shift_3_3'] = (-0.20, -0.148)
    # Center-point for text on canvas with respect to whole canvas
    properties['text_player1'] = (0.25, 0.076)
    properties['text_player2'] = (0.75, 0.076)
    properties['text_event'] = (0.25, 0.924)
    properties['text_round'] = (0.75, 0.924)
    properties['text_angle'] = 2  # degree of rotation counter-clockwise
    properties['event_round_single_text'] = False  # Flag to determine if the event and round text is combined
    properties['event_round_text_split'] = ' '  # Text for between event and round when a single element
    # Font settings
    properties['font_location'] = os.path.join("Fonts", "tt2004m.ttf")
    properties['font_player1_size'] = 45
    properties['font_player2_size'] = 45
    properties['font_event_size'] = 45
    properties['font_round_size'] = 45
    properties['font_color1'] = '#F5F5F5'  # (245, 245, 245)
    properties['font_color2'] = '#F5F5F5'  # (245, 245, 245)
    properties['font_color3'] = '#F5F5F5'  # (245, 245, 245)
    properties['font_color4'] = '#F5F5F5'  # (245, 245, 245)
    # Border Filter settings
    properties['font_glow_bool'] = False  # Flag to apply glow to font
    properties['font_glow_color'] = '#050505'  # (5, 5, 5)
    properties['font_glow_px'] = 3  # Pixel count for the blur in all directions
    properties['font_glow_itr'] = 25  # Iterations on applying filter
    properties['font_glow_offset'] = (0, 3)  # Offset to apply the filtered effect
    # Character Pixelation filter to characters
    properties['pixelate_filter_bool'] = False  # Flag to pixelate the characters
    properties['pixelate_filter_size'] = 16  # size of pixel squares
    # Useful flags
    properties['show_first_image'] = True  # Flag for showing one sample image when generating
    properties['one_char_flag'] = True  # Flag to determine if there is only one character on the overlay or multiple

    # return properties
    return properties


def setGlobalsQuarantainment(number):
    """
    Set necessary globals for Quarantainment event {number} for create_thumbnail.py
    properties dictionary is fed in, modified, then returned
    :param number:
    :return:
    """
    # Load in default
    properties = set_default_properties()
    # Character renders folder location
    properties['render_type'] = "Full render"
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'Quarantainment {s} names.txt'.format(s=number))
    # Background and Foreground overlay locations
    properties['background_file'] = os.path.join('Overlays', 'Background_Q.png')
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground_Q.png')
    # Canvas flag
    properties['char_glow_bool'] = True
    # Center-point shift for canvas for characters
    properties['center_shift_1'] = (-0.04, +0.01)
    properties['char_border'] = (0.00, 0.26)  # border for characters
    properties['resize_1'] = 0.85  # resize for character for multiple renders on image
    properties['resize_2'] = 0.75
    properties['resize_3'] = 0.60
    # Single character flag on overlay
    properties['one_char_flag'] = False
    # Return with modifications
    return properties


def setGlobalsSxT(number):
    """
    Set necessary globals for Students x Treehouse event {number} for create_thumbnail.py
    properties dictionary is fed in, modified, then returned
    :param number:
    :return:
    """
    # Set to Quaratainment settings and then adjust
    properties = setGlobalsQuarantainment(number)
    #
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'Students x Treehouse {s} names.txt'.format(s=number))
    # Foreground overlay locations
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground_SxT.png')
    # Return with modifications
    return properties


def setGlobalsFro(number):
    """
    Set all globals for Fro Friday event {number} for create_thumbnail.py
    properties dictionary is fed in, modified, then returned
    :param number:
    :return:
    """
    # Load in default
    properties = set_default_properties()
    # Character renders folder location
    properties['render_type'] = "Full render"
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'Fro Fridays {s} names.txt'.format(s=number))
    # Background and Foreground overlay locations
    #properties['background_file'] = os.path.join('Overlays', 'Background_Fro.png')
    properties['background_file'] = os.path.join('Overlays', 'Background_Fro2.png')
    #properties['foreground_file'] = os.path.join('Overlays', 'Foreground_Fro.png')
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground_Fro2.png')
    # Single character flag on overlay
    properties['one_char_flag'] = True
    # Scaler Variables for characters in window
    properties['resize_1'] = 1.00
    # Center-point shift for canvas for characters
    properties['center_shift_1'] = (-0.00, +0.00)  # Universal character shift
    properties['char_border'] = (0.00, 0.26)  # border for characters
    # Center-point for text on canvas with respect to whole canvas
    properties['text_player1'] = (0.23, 0.75)  # (0.20, 0.75)
    properties['text_player2'] = (0.77, 0.75)  # (0.80, 0.75)
    properties['text_event'] = (0.50, 0.075)
    properties['text_round'] = (0.50, 0.075)
    properties['text_angle'] = 0  # degree of rotation counter-clockwise
    # Font settings
    #properties['font_location'] = os.path.join("Fonts", "LostLeonestReguler-MVVMn.otf")
    properties['font_location'] = os.path.join("Fonts", "Molot.otf")
    properties['font_player1_size'] = 65  #42
    properties['font_player2_size'] = 65  #42
    properties['font_event_size'] = 45  #37
    properties['font_round_size'] = 45  #37
    properties['font_glow_bool'] = True
    properties['font_glow_color'] = '#101010'  # '#641fbf'  # (100, 31, 191)
    properties['font_glow_px'] = 2  # Pixel count for the blur in all directions
    properties['font_glow_itr'] = 25  # Iterations on applying filter
    properties['font_glow_offset'] = (0, 0)  # Offset to apply the filtered effect
    # Combined event and round text
    properties['event_round_single_text'] = True
    properties['event_round_text_split'] = ' - '
    # Return with modifications
    return properties


def setGlobalsAWG(number):
    """
    Set all globals for AWG event {number} for create_thumbnail.py
    properties dictionary is fed in, modified, then returned
    :param number:
    :return:
    """
    # Load in default
    properties = set_default_properties()
    # Character renders folder location
    properties['render_type'] = "Full render"
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'AWG {s} names.txt'.format(s=number))
    # Background and Foreground overlay locations
    properties['background_file'] = os.path.join('Overlays', 'Background_AWG.png')
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground_AWG_spring.png')
    # Character border settings
    properties['char_border'] = (0.00, 0.35)  # border for characters
    properties['char_offset1'] = (0, -0.00)  # offset for left player window placement on canvas
    properties['char_offset2'] = (0.5, -0.00)  # offset for right player window placement on canvas
    # Single character flag on overlay
    properties['one_char_flag'] = True
    # Scaler Variables for characters in window
    properties['resize_1'] = 1.00
    # Center-point shift for canvas for characters
    properties['center_shift_1'] = (+0.03, -0.03)  # Universal character shift
    # Center-point for text on canvas with respect to whole canvas
    properties['text_player1'] = (0.25, 0.70)
    properties['text_player2'] = (0.70, 0.70)
    properties['text_event'] = (0.50, 0.10)
    properties['text_round'] = (0.50, 0.10)
    properties['text_angle'] = 0  # degree of rotation counter-clockwise
    # Font settings
    properties['font_location'] = os.path.join("Fonts", "ConnectionIi-2wj8.otf")
    properties['font_player1_size'] = 42
    properties['font_player2_size'] = 42
    properties['font_event_size'] = 42
    properties['font_round_size'] = 42
    properties['font_glow_bool'] = True
    properties['font_filter_px'] = 2  # Pixel count for the blur in all directions
    properties['font_filter_itr'] = 15  # Iterations on applying filter
    properties['font_filter_offset'] = (0, 1)  # Offset to apply the filtered effect
    # Character Pixelation filter to characters
    properties['pixelate_filter_bool'] = True  # Flag to pixelate the characters
    properties['pixelate_filter_size'] = 280  # size of pixel squares
    # Combined event and round text
    properties['event_round_single_text'] = True
    properties['event_round_text_split'] = ' - '
    # Return with modifications
    return properties


def setGlobalsC2C(number):
    """
    Set necessary globals for Students x Treehouse event {number} for create_thumbnail.py
    properties dictionary is fed in, modified, then returned
    :param number:
    :return:
    """
    # Set to Quaratainment settings and then adjust
    properties = setGlobalsQuarantainment(number)
    #
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'C2C Finale {s} names.txt'.format(s=number))
    # Background and Foreground overlay locations
    properties['background_file'] = os.path.join('Overlays', 'Background_C2C.png')
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground_C2C.png')
    # Single character flag on overlay
    properties['one_char_flag'] = True
    properties['resize_1'] = 1.0
    # Return with modifications
    return properties


def setGlobalsCatman(number):
    """
    Set necessary globals for Catman event {number} for create_thumbnail.py
    properties dictionary is fed in, modified, then returned
    :param number:
    :return:
    """
    # Set to Quaratainment settings and then adjust
    properties = setGlobalsQuarantainment(number)
    #
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'Catman {s} names.txt'.format(s=number))
    # Foreground overlay locations
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground_Catman.png')
    # Return with modifications
    return properties


def setGlobalsQuarantainment_Top8():
    """
    Set necessary globals for Quarantainment Top 8 Graphic for create_top8_graphic.py
    properties dictionary is fed in, modified, then returned
    :return:
    """
    # Load in default
    properties = set_default_properties()
    # Character renders folder location
    properties['render_type'] = "Body render"
    properties['render_type2'] = "Diamond render"
    # Event match file information location
    properties['top8_info'] = os.path.join('..', 'Vod Names', '_top8_test.txt')
    # Background and Foreground overlay locations
    properties['background_file'] = os.path.join('Top8_Graphics', 'Jetstream_Top8_Background.png')
    properties['foreground_file'] = os.path.join('Top8_Graphics', 'Jetstream_Top8_Foreground.png')
    # Canvas flag
    properties['char_glow_bool'] = True
    # Center-point shift for canvas for characters
    properties['resize_1'] = 1.0
    properties['resize_2'] = 0.75
    # Placements for windows
    properties['char_window'] = (0.33, 0.25)  # canvas for characters
    properties['char_offset1'] = (0.00, 0.00)  # Offset for 1
    properties['char_offset2'] = (0.00, 0.25)  # Offset for 2
    properties['char_offset3'] = (0.00, 0.50)  # Offset for 3
    properties['char_offset4'] = (0.00, 0.75)  # Offset for 4
    properties['char_offset5'] = (0.33, 0.00)  # Offset for 5
    properties['char_offset6'] = (0.33, 0.25)  # Offset for 6
    properties['char_offset7'] = (0.33, 0.50)  # Offset for 7
    properties['char_offset8'] = (0.33, 0.75)  # Offset for 8
    # Center-point shift for canvas for characters
    properties['center_shift_1'] = (-0.00, +0.10)  # Universal character shift
    properties['center_shift_2_1'] = (-0.20, +0.11)  # Two character shift
    properties['center_shift_2_2'] = (+0.20, -0.11)
    properties['center_shift_3_1'] = (-0.15, +0.148)  # Three character shift
    properties['center_shift_3_2'] = (+0.25, -0.037)
    properties['center_shift_3_3'] = (-0.20, -0.148)
    # Player Font settings
    properties['text_angle'] = 0
    properties['font_player_location'] = os.path.join("Fonts", "BungeeInline-Regular.ttf")
    properties['font_player_color'] = '#F5F5F5'  # (245, 245, 245)
    properties['font_player_align'] = 'left'
    properties['font_player_size'] = 48
    properties['font_player1_offset'] = (0.05, 0.05)  # Offset for 1
    properties['font_player2_offset'] = (0.05, 0.30)  # Offset for 2
    properties['font_player3_offset'] = (0.05, 0.55)  # Offset for 3
    properties['font_player4_offset'] = (0.05, 0.80)  # Offset for 4
    properties['font_player5_offset'] = (0.38, 0.05)  # Offset for 5
    properties['font_player6_offset'] = (0.38, 0.30)  # Offset for 6
    properties['font_player7_offset'] = (0.38, 0.55)  # Offset for 7
    properties['font_player8_offset'] = (0.38, 0.80)  # Offset for 8
    # Twitter Font settings
    properties['font_twitter_location'] = os.path.join("Fonts", "arial.ttf")
    properties['font_twitter_color'] = '#F5F5F5'  # (245, 245, 245)
    properties['font_twitter_back_color'] = '#00000025'  # (0, 0, 0, 25)
    properties['font_twitter_align'] = 'right'
    properties['font_twitter_size'] = 24
    properties['font_twitter1_offset'] = (0.30, 0.20)  # Offset for 1
    properties['font_twitter2_offset'] = (0.30, 0.45)  # Offset for 2
    properties['font_twitter3_offset'] = (0.30, 0.70)  # Offset for 3
    properties['font_twitter4_offset'] = (0.30, 0.95)  # Offset for 4
    properties['font_twitter5_offset'] = (0.63, 0.20)  # Offset for 5
    properties['font_twitter6_offset'] = (0.63, 0.45)  # Offset for 6
    properties['font_twitter7_offset'] = (0.63, 0.70)  # Offset for 7
    properties['font_twitter8_offset'] = (0.63, 0.95)  # Offset for 8


    # Additional Font information for event info
    properties['font_event_location'] = os.path.join("Fonts", "tt2004m.ttf")
    properties['font_event_size'] = 45
    properties['font_data_location'] = os.path.join("Fonts", "tt2004m.ttf")
    properties['font_date_size'] = 45


    # Return with modifications
    return properties


def setGlobalsSxT_Top8():
    """
    Set necessary globals for Students x Treehouse Top 8 Graphic for create_top8_graphic.py
    properties dictionary is fed in, modified, then returned
    :return:
    """
    # Set to Quaratainment settings and then adjust
    properties = setGlobalsQuarantainment_Top8()
    #
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'Students x Treehouse {s} names.txt'.format(s=number))
    # Foreground overlay locations
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground_SxT.png')
    # Return with modifications
    return properties
"""
Script to set globals needed for create_thumbnail
"""
import os


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
    properties['char_window'] = (0.5, 1)  # canvas for characters
    properties['char_border'] = (0.00, 0.26)  # border for characters
    properties['char_offset1'] = (0, 0.00)  # offset for left player window placement on canvas
    properties['char_offset2'] = (0.5, 0.00)  # offset for right player window placement on canvas
    # Scaler Variables for characters in window
    properties['resize_1'] = 1.65  # resize for character for multiple renders on image
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


def setGlobalsQuarantainment(properties, number):
    """
    Set necessary globals for Quarantainment event {number} for create_thumbnail.py
    properties dictionary is fed in, modified, then returned
    :param properties:
    :param number:
    :return:
    """
    # Character renders folder location
    properties['render_type'] = "Full render"
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'Quarantainment {s} names.txt'.format(s=number))
    # Background and Foreground overlay locations
    properties['background_file'] = os.path.join('Overlays', 'Background_Q.png')
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground_Q.png')
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


def setGlobalsSxT(properties, number):
    """
    Set necessary globals for Students x Treehouse event {number} for create_thumbnail.py
    properties dictionary is fed in, modified, then returned
    :param properties:
    :param number:
    :return:
    """
    # Set to Quaratainment settings and then adjust
    properties = setGlobalsQuarantainment(properties, number)
    #
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'Students x Treehouse {s} names.txt'.format(s=number))
    # Foreground overlay locations
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground_SxT.png')
    # Return with modifications
    return properties


def setGlobalsFro(properties, number):
    """
    Set all globals for Fro Friday event {number} for create_thumbnail.py
    properties dictionary is fed in, modified, then returned
    :param properties:
    :param number:
    :return:
    """
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


def setGlobalsAWG(properties, number):
    """
    Set all globals for AWG event {number} for create_thumbnail.py
    properties dictionary is fed in, modified, then returned
    :param properties:
    :param number:
    :return:
    """
    # Character renders folder location
    properties['render_type'] = "Full render"
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'AWG {s} names.txt'.format(s=number))
    # Background and Foreground overlay locations
    properties['background_file'] = os.path.join('Overlays', 'Background_AWG.png')
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground_AWG.png')
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


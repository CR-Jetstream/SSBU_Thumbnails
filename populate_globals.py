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
    # Event match file information location
    properties['event_info'] = os.path.join('..', 'Vod Names', 'Sample test names.txt')
    # Background and Foreground overlay locations
    properties['background_file'] = os.path.join('Overlays', 'Background.png')
    properties['foreground_file'] = os.path.join('Overlays', 'Foreground.png')
    # Output save location
    properties['save_location'] = os.path.join('..', 'Youtube_Thumbnails')
    # Canvas variables for character window with respect to whole canvas
    properties['char_window'] = (0.5, 1)  # canvas for characters
    properties['char_border'] = (0.00, 0.26)  # border for characters
    properties['char_offset1'] = (0, 0.00)  # offset for left player window placement on canvas
    properties['char_offset2'] = (0.5, 0.00)  # offset for right player window placement on canvas
    # Scaler Variables for multiple characters in window
    properties['resize_1'] = 0.85  # resize for character for multiple renders on image
    properties['resize_2'] = 0.75
    properties['resize_3'] = 0.60
    # Center-point shift for canvas for characters
    properties['center_shift_1'] = (-0.04, +0.01)  # Universal character shift
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
    # Font settings
    properties['font_location'] = os.path.join("Fonts", "tt2004m.ttf")
    properties['font_size'] = 45
    properties['font_color1'] = '#F5F5F5'  # (245, 245, 245)
    properties['font_color2'] = '#F5F5F5'  # (245, 245, 245)
    properties['font_color3'] = '#F5F5F5'  # (245, 245, 245)
    properties['font_color4'] = '#F5F5F5'  # (245, 245, 245)
    properties['font_filter_color'] = '#050505'  # (5, 5, 5)
    properties['font_filter_px'] = 3  # Pixel count for the blur in all directions
    properties['font_filter_itr'] = 25  # Iterations on applying filter
    properties['font_filter_offset'] = (0, 3)  # Offset to apply the filtered effect
    # Useful flags
    properties['show_first_image'] = True  # Flag for showing one sample image when generating
    properties['one_char_flag'] = False  # Flag to determine if there is only one character on the overlay or multiple
    properties['event_round_single_text'] = False  # Flag to determine if the event and round text is combined
    properties['event_round_text_split'] = ' '  # Text for between event and round when a single element
    properties['font_glow_bool'] = False  # Flag to apply glow to font

    # return properties
    return properties


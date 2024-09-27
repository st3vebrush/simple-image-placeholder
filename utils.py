#  Copyright (c) 2024
#  by St3vebrush with love for D3velopment

import html
import io
import re

# utils.py
from PIL import Image, ImageColor, ImageDraw, ImageFont
from flask import send_file

"""
Default configuration dictionary for the application.

This dictionary contains the default values for various configuration parameters used in the application.
These values are used to validate and set the configuration parameters if they are not provided or are invalid.

Keys:
- MAX_WIDTH (int): The maximum width allowed for images.
- MAX_HEIGHT (int): The maximum height allowed for images.
- DEFAULT_WIDTH (int): The default width for images.
- DEFAULT_HEIGHT (int): The default height for images.
- MAX_FONT_SIZE (int): The maximum font size allowed.
- MIN_FONT_SIZE (int): The minimum font size allowed.
- DEFAULT_FONT_SIZE (int): The default font size.
- MAX_TEXT_LENGTH (int): The maximum length allowed for text.
- DEFAULT_BG_COLOR (str): The default background color for images. (e.g., 'grey', 'red', 'green', 'blue', etc. or #RGB or #RRGGBB or hex color codes)
- DEFAULT_TEXT (str): The default text to be displayed on images.
- DEFAULT_FORMAT (str): The default format for images (e.g., 'jpeg', 'png', 'webp', 'svg').
- MAX_REQUESTS_PER_MINUTES (int): The maximum number of requests allowed per minute.
"""
default_config = {
    'MAX_WIDTH': 1920,
    'MAX_HEIGHT': 1080,
    'DEFAULT_WIDTH': 320,
    'DEFAULT_HEIGHT': 200,
    'MAX_FONT_SIZE': 100,
    'MIN_FONT_SIZE': 1,
    'DEFAULT_FONT_SIZE': 30,
    'MAX_TEXT_LENGTH': 255,
    'DEFAULT_BG_COLOR': 'grey',
    'DEFAULT_TEXT': 'Hello, World!',
    'DEFAULT_FORMAT': 'webp',
    'MAX_REQUESTS_PER_MINUTES': 100
}


def validate_config(config):
    """
    Validates the configuration dictionary against predefined rules.

    This function checks each key-value pair in the configuration dictionary against a set of validation rules.
    If a value does not meet the validation criteria, it prints a warning message and sets the value to the default.

    Parameters:
    - config (dict): The configuration dictionary to be validated.
    Validation Rules:
    - MAX_WIDTH (int): Must be a positive integer.
    - MAX_HEIGHT (int): Must be a positive integer.
    - DEFAULT_WIDTH (int): Must be a positive integer.
    - DEFAULT_HEIGHT (int): Must be a positive integer.
    - MAX_FONT_SIZE (int): Must be a positive integer.
    - MIN_FONT_SIZE (int): Must be a positive integer.
    - DEFAULT_FONT_SIZE (int): Must be a positive integer.
    - MAX_TEXT_LENGTH (int): Must be a positive integer.
    - MAX_REQUESTS_PER_MINUTES (int): Must be a positive integer.
    - DEFAULT_BG_COLOR (str): Must be a valid color name or hex color code.
    - DEFAULT_TEXT (str): Must be a string.
    - DEFAULT_FORMAT (str): Must be one of 'jpeg', 'png', 'webp', or 'svg'.

    Returns:
    - None
    """
    validation_rules = {
        'MAX_WIDTH': lambda x: isinstance(x, int) and x > 0,
        'MAX_HEIGHT': lambda x: isinstance(x, int) and x > 0,
        'DEFAULT_WIDTH': lambda x: isinstance(x, int) and x > 0,
        'DEFAULT_HEIGHT': lambda x: isinstance(x, int) and x > 0,
        'MAX_FONT_SIZE': lambda x: isinstance(x, int) and x > 0,
        'MIN_FONT_SIZE': lambda x: isinstance(x, int) and x > 0,
        'DEFAULT_FONT_SIZE': lambda x: isinstance(x, int) and x > 0,
        'MAX_TEXT_LENGTH': lambda x: isinstance(x, int) and x > 0,
        'MAX_REQUESTS_PER_MINUTES': lambda x: isinstance(x, int) and x > 0,
        'DEFAULT_BG_COLOR': lambda x: isinstance(x, str) and (
                x in ImageColor.colormap or re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', x)),
        'DEFAULT_TEXT': lambda x: isinstance(x, str),
        'DEFAULT_FORMAT': lambda x: x in ['jpeg', 'png', 'webp', 'svg'],
    }

    for key, rule in validation_rules.items():
        if not rule(config.get(key, default_config[key])):
            print(f'⚠️ Warning: Invalid value for {key} = {config[key]}. Using default value: {default_config[key]}')
            config[key] = default_config[key]


def validate_input(args, config, default_font):
    width = args.get('width', default=config['DEFAULT_WIDTH'], type=int)
    height = args.get('height', default=config['DEFAULT_HEIGHT'], type=int)
    text = args.get('text', default=config['DEFAULT_TEXT'], type=str)
    text = html.escape(text)[:config['MAX_TEXT_LENGTH']]
    font_size = args.get('font_size', default=config['DEFAULT_FONT_SIZE'], type=int)
    background_color = args.get('bg_color', default=config['DEFAULT_BG_COLOR'], type=str)
    export_format = args.get('format', default=config['DEFAULT_FORMAT'], type=str).lower()

    error_response = validate_width(width, config)
    if error_response:
        return error_response

    error_response = validate_height(height, config)
    if error_response:
        return error_response
    print(font_size)
    error_response = validate_font_size(font_size, config)
    if error_response:
        return error_response

    error_response = validate_background_color(background_color)
    if error_response:
        return error_response

    error_response = validate_export_format(export_format)
    if error_response:
        return error_response

    return width, height, text, font_size, background_color, export_format


def check_hex_color(color):
    """
    Checks if the provided color is a valid hex color code and formats it correctly.

    This function checks if the input color string is a valid hex color code (either 3 or 6 characters long).
    If the color string is valid, it appends a '#' character to the beginning of the string to ensure it is a valid hex color code.
    Otherwise, returns the color string as is : color is a valid color name.

    Parameters:
    - color (str): The color string to be checked.

    Returns:
    - str: The formatted hex color code with a '#' prefix if the input is a valid hex color code.
    """
    if re.match(r'^[0-9a-fA-F]{3}$|^[0-9a-fA-F]{6}$', color):
        color = '#' + color
    return color


def sanitize_for_svg(text):
    text = re.sub(r'<[^>]*>', '', text)
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return text


def generate_error_image(width, height, error_message, config):
    """
    Generates an error image with the specified dimensions and error message.

    This function creates an image with a red background and a black error message centered in the image.
    The dimensions of the image are determined by the provided width and height, but they are adjusted
    to be at least as large as the default width and height specified in the configuration.

    Parameters:
    - width (int): The width of the error image.
    - height (int): The height of the error image.
    - error_message (str): The error message to be displayed on the image.
    - config (dict): The configuration dictionary containing default values.

    Returns:
    - Flask response object: An image file with the error message.
    """

    # Ensure the width and height are at least the default values
    width = max(width, config['DEFAULT_WIDTH'])
    height = max(height, config['DEFAULT_HEIGHT'])

    # Create a new image with a red background
    image = Image.new('RGB', (width, height), color='#FF8888')

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Load the default font and set the font size
    font = ImageFont.load_default().font_variant(size=20)

    # Calculate the bounding box of the text to determine its width and height
    bbox = draw.textbbox((0, 0), error_message, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate the position to center the text
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Adjust the y-coordinate to vertically center the text
    ascent, descent = font.getmetrics()
    y -= ascent / 2 - descent / 2

    # Draw the error message on the image
    draw.text((x, y), error_message, font=font, fill='black')

    # Save the image to a BytesIO object
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    # Return the image as a Flask response object
    return send_file(img_io, mimetype='image/png')


def validate_width(width, config):
    if width < 1 or width > config['MAX_WIDTH']:
        return generate_error_image(
            config['DEFAULT_WIDTH'],
            config['DEFAULT_HEIGHT'],
            f"Invalid width.\nWidth must be a positive integer\nbetween 1 and {config['MAX_WIDTH']}.",
            config
        )
    return None


def validate_height(height, config):
    if height < 1 or height > config['MAX_HEIGHT']:
        return generate_error_image(
            config['DEFAULT_WIDTH'],
            config['DEFAULT_HEIGHT'],
            f"Invalid height.\nHeight must be a positive integer\nbetween 1 and {config['MAX_HEIGHT']}.",
            config
        )
    return None


def validate_font_size(font_size, config):
    if font_size < 1 or font_size > config['MAX_FONT_SIZE']:
        return generate_error_image(
            config['DEFAULT_WIDTH'],
            config['DEFAULT_HEIGHT'],
            f"Invalid font size.\nFont size must be a positive integer\nbetween 1 and {config['MAX_FONT_SIZE']}.",
            config
        )
    return None


def validate_background_color(background_color):
    try:
        ImageColor.getrgb(background_color)
    except ValueError:
        if not re.match(r'^(?:[0-9a-fA-F]{3}){1,2}$', background_color):
            return generate_error_image(
                default_config['DEFAULT_WIDTH'],
                default_config['DEFAULT_HEIGHT'],
                "Invalid background color.\nBackground color must be\na valid named color\nor a valid hex color.",
                default_config
            )
    return None


def validate_export_format(export_format):
    if export_format not in ['jpeg', 'png', 'webp', 'svg']:
        return generate_error_image(
            default_config['DEFAULT_WIDTH'],
            default_config['DEFAULT_HEIGHT'],
            "Invalid format.\nmust be one of the following:\njpeg, png, webp, or svg.",
            default_config
        )
    return None

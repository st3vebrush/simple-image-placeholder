#  Copyright (c) 2024
#  by St3vebrush <steve@d3velopment.fr> with love for D3velopment

# app.py

import io
import os

import svgwrite
from PIL import Image, ImageDraw, ImageFont, ImageColor
from flask import Flask, request, send_file, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils import (
    default_config,
    validate_config,
    sanitize_for_svg,
    check_hex_color,
    validate_input
)

app = Flask(__name__)
"""
Initialization and Configuration
"""

# Load configuration from config.py or environment variables
app.config.from_object('config')

# Override with environment variables if present
for key in default_config.keys():
    if key in os.environ:
        app.config[key] = os.environ[key]

# Set default values if not present in config or environment variables
for key, value in default_config.items():
    if key not in app.config:
        app.config[key] = value
        print(
            f"⚠️ Warning: Could not find {key} constant, neither in config or as environment variable. Using default value : {value}")

# Convert string values to integers where applicable
for key in ['MAX_WIDTH', 'MAX_HEIGHT', 'DEFAULT_WIDTH', 'DEFAULT_HEIGHT', 'MAX_FONT_SIZE', 'MIN_FONT_SIZE',
            'DEFAULT_FONT_SIZE', 'MAX_TEXT_LENGTH', 'MAX_REQUESTS_PER_MINUTES']:
    try:
        app.config[key] = int(app.config[key])
    except ValueError:
        print(
            f'⚠️ Warning: Could not convert {key} = {str(app.config[key])} to integer. Setting to default value : {str(default_config[key])}')
        app.config[key] = default_config[key]

# Validate the configuration
validate_config(app.config)

# Initialize the rate limiter
limiter = Limiter(get_remote_address, app=app, storage_uri="memory://")

# Load the default font
default_font = ImageFont.load_default()

"""
Routes
"""


@app.route('/favicon.ico')
def favicon():
    """
    Serve the favicon.ico file.

    Returns:
    - Flask response: The favicon.ico file with the appropriate MIME type.
    """
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/help')
def help():
    """
    Serve the help file.

    Returns:
    - Flask response: The help file with the appropriate MIME type.
    """
    return send_from_directory(app.root_path, 'help.html', mimetype='text/html')


@app.route('/robots.txt')
def noindex():
    """
    Serve the robots.txt file to disallow web crawling.

    This endpoint returns a robots.txt file that instructs web crawlers to disallow
    crawling of the entire site and sets a crawl delay of 60 seconds.
    Returns:
    - Flask response: The robots.txt file with the appropriate MIME type.
    """
    return send_from_directory(app.root_path, 'robots.txt', mimetype='text/plain')


@app.route('/', methods=['GET'])
@limiter.limit(f"{app.config['MAX_REQUESTS_PER_MINUTES']} per minute")
def generate():
    """
    Generate an image based on the input parameters provided via the query string.

    Main endpoint that generates an image based on the input parameters provided,
    including width, height, text, font size, background color, and export format.
    The parameters are validated, sanitized, and used to generate the image.

    Returns:
    - Flask response: The generated image in the specified format.
    """
    # Validate the input parameters from the request
    validation_result = validate_input(request.args, app.config, default_font)

    # Check if the validation result is a tuple containing valid parameters
    if isinstance(validation_result, tuple):
        # Unpack the validated parameters from the tuple
        width, height, text, font_size, background_color, export_format = validation_result
    else:
        # If the validation result is not a tuple, it means there was an error
        # Return the validation result, which could be an error message or response
        return validation_result

    # Ensure the background color is in the correct format
    background_color = check_hex_color(background_color)

    # Determine the font color based on the background color's brightness
    font_color = 'white' if ImageColor.getcolor(background_color, 'L') <= 128 else 'black'

    font = default_font.font_variant(size=font_size)

    # Generate and return the image in the specified format
    if export_format == 'svg':
        return generate_svg(width, height, text, font_size, background_color, font_color, font)
    else:
        return generate_raster_image(width, height, text, font_size, background_color, export_format, font_color, font)


def generate_raster_image(width, height, text, font_size, background_color, export_format, font_color, font):
    """
    Generate a raster image based on the input parameters provided.

    Parameters:
    - width (int): The width of the image.
    - height (int): The height of the image.
    - text (str): The text to be displayed on the image.
    - font_size (int): The font size of the text.
    - background_color (str): The background color of the image.
    - export_format (str): The format of the exported image (e.g., 'png', 'jpg').
    - font_color (str): The color of the font.

    Returns:
    - Flask response: The generated raster image.
    """

    # Create a new image with the specified dimensions and background color
    image = Image.new('RGB', (width, height), color=background_color)

    # Create a drawing context for the image
    draw = ImageDraw.Draw(image)

    # Calculate the bounding box of the text to determine its width and height
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate the position of the text to center it on the image
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Adjust the y-coordinate based on the font metrics to vertically center the text
    ascent, descent = font.getmetrics()
    y -= ascent / 2 - descent / 2

    # Draw the text on the image with the specified font color
    draw.text((x, y), text, font=font, fill=font_color)

    # Save the image to a BytesIO object in the specified format
    img_io = io.BytesIO()
    image.save(img_io, export_format.upper())
    img_io.seek(0)

    # Return the image as a Flask response with the appropriate MIME type
    return send_file(img_io, mimetype=f'image/{export_format}')


def generate_svg(width, height, text, font_size, background_color, font_color, font):
    """
    Generate an SVG image based on the input parameters provided.

    Parameters:
    - width (int): The width of the image.
    - height (int): The height of the image.
    - text (str): The text to be displayed on the image.
    - font_size (int): The font size of the text.
    - background_color (str): The background color of the image.

    Returns:
    - Flask response: The generated SVG image.
    """

    # Create a new SVG drawing
    dwg = svgwrite.Drawing('', profile='tiny', size=(width, height))

    # Add the background rectangle
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill=background_color))

    # Calculate the position of the text based on the font metrics
    ascent, descent = font.getmetrics()
    text_height = ascent - descent
    y = (height - text_height + ascent) / 2

    # Add the text element
    # Sanitize the text to remove any XML tags and encode special characters
    text = sanitize_for_svg(text)
    dwg.add(dwg.text(text, insert=('50%', y), text_anchor="middle", font_size=font_size, fill=font_color))

    # Save the SVG drawing to a BytesIO object
    svg_data = dwg.tostring().encode()
    svg_io = io.BytesIO(svg_data)

    return send_file(svg_io, mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run(debug=True)

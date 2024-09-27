#  Copyright (c) 2024
#  by St3vebrush with love for D3velopment

# config.py

# Maximum dimensions for the generated image
MAX_WIDTH = 1920  # Maximum width in pixels
MAX_HEIGHT = 1080  # Maximum height in pixels

# Default dimensions for the generated image
DEFAULT_WIDTH = 320  # Default width in pixels
DEFAULT_HEIGHT = 200  # Default height in pixels

# Font size limits
MAX_FONT_SIZE = 100  # Maximum font size for the text on the generated image
MIN_FONT_SIZE = 1  # Minimum font size for the text on the generated image
DEFAULT_FONT_SIZE = 30  # Default font size for the text on the generated image

# Maximum length for the text on the image
MAX_TEXT_LENGTH = 255  # Maximum number of characters for the text on the image

# Default settings for the image
DEFAULT_BG_COLOR = 'bisque'  # Default background color for the image. Accepts hex color codes or color names (e.g., '#FF0000', '#F00', or 'red'). Warning : The bg_color query parameter used in the URL must be without the '#'.
DEFAULT_TEXT = 'Hello, World!'  # Default text to display on the image, leave empty for no text
DEFAULT_FORMAT = 'webp'  # Default format for the image, can be jpeg, png, webp, or svg. webp is modern and highly compressed, it is recommended for its balance of quality and size and is far better than jpeg.

# Rate limiting
MAX_REQUESTS_PER_MINUTES = 100  # Maximum number of requests allowed per minute to prevent abuse

# Simple Image Placeholder

Simple Image Placeholder is a web-based application designed to generate placeholder images based on input parameters
provided via the query string. These images can be used in HTML `<img>` tags to serve as placeholders until the actual
images are available. The query string contains key-value pairs that specify the width, height, text, font size,
background color, and export format of the desired image. It supports PNG, JPEG, WEBP, and SVG image formats.

## Features

- Generate placeholder images with customizable width, height, text, font size, background color, and export format.
- Validation and sanitization of input parameters.
- Error handling and generation of error images.
- Rate limiting to prevent abuse.
- Support for PNG, JPEG, WEBP, and SVG formats - defaults to WEBP.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/st3vebrush/simple-image-placeholder.git
   ```

2. Navigate to the project directory:

   ```bash
   cd simple-image-placeholder
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

The application will be accessible at `http://localhost:5000`.

## Usage

To generate an image, make a GET request to the root URL (`/`) with the desired parameters in the query string. For
example:

```html
<img src="http://localhost:5000/?width=800&height=600&text=Hello!&font_size=40&bg_color=blue&format=png"
     alt="great image placeholder">
```

This will generate a PNG image with the text "Hello!" on a blue background, with a font size of 40, and dimensions of
800x600 pixels.

## Configuration

The application's configuration is defined in the `config.py` file. You can customize various parameters to suit your
needs. Here are the available configuration options:

- `MAX_WIDTH`: Maximum width allowed for images. Default is 1920 pixels.
- `MAX_HEIGHT`: Maximum height allowed for images. Default is 1080 pixels.
- `DEFAULT_WIDTH`: Default width for images. Default is 320 pixels.
- `DEFAULT_HEIGHT`: Default height for images. Default is 200 pixels.
- `MAX_FONT_SIZE`: Maximum font size allowed. Default is 100.
- `MIN_FONT_SIZE`: Minimum font size allowed. Default is 1.
- `DEFAULT_FONT_SIZE`: Default font size. Default is 30.
- `MAX_TEXT_LENGTH`: Maximum length allowed for text. Default is 255 characters.
- `DEFAULT_BG_COLOR`: Default background color for images. Accepts hex color codes or color names (e.g., '#FF0000', '
  #F00', or 'red'). Default is 'bisque'.
- `DEFAULT_TEXT`: Default text to be displayed on images. Default is 'Hello, World!'.
- `DEFAULT_FORMAT`: Default format for images. Can be 'jpeg', 'png', 'webp', or 'svg'. Default is 'webp'.
- `MAX_REQUESTS_PER_MINUTES`: Maximum number of requests allowed per minute to prevent abuse. Default is 100.

**Additionally, you can override these configuration parameters by setting environment variables with the same names.**

### Example of environment variable override

Let's say you want to change the default background color to 'lightblue' and the maximum width to 2000 pixels.
Instead of modifying the `config.py` file, you can set these values as environment variables.

For Unix-based systems (Linux, macOS), you can use the `export` command to set environment variables:

```bash
export DEFAULT_BG_COLOR=lightblue
export MAX_WIDTH=2000
```

For Windows, you can use the `set` command:

```cmd
set DEFAULT_BG_COLOR=lightblue
set MAX_WIDTH=2000
```

After setting these environment variables, you can run the application as usual:

```bash
python app.py
```

Application will use the values of the environment variables instead of the values defined in the `config.py` file.

Also, it can be launched as a single line

```bash
DEFAULT_BG_COLOR=lightblue MAX_WIDTH=2000 python app.py
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a
pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

"""
File: final_project.py
----------------
This program applies a filter to images to make them look like they are displayed on a monochrome Apple II monitor.
"""
from PIL import Image

APPLE_II_WIDTH_ACTUAL = 560  # Actual pixel width of an Apple II screen
APPLE_II_HEIGHT_PERCEIVED = 384  # Visual height of Apple II screen
APPLE_II_HEIGHT_ACTUAL = 192  # Actual pixel height of Apple II screen
MONOCHROME_POSITIVE_TUPLE = (107, 196, 71)  # RGB values that approximate the appearance of a green monochrome monitor's positive space
MONOCHROME_NEGATIVE_TUPLE = (16, 29, 11)  # RGB values that approximate the appearance of a green monochrome monitor's negative space

DEFAULT_FILE = 'images/balldog.jpg'

def main():
    """
    Takes a single file as input, shows the original, and shows a copy with the filter applied
    """
    # Get file and load image
    filename = get_file()
    image = Image.open(filename)

    # Show the original image
    original_image = Image.open(filename)
    original_image.show()

    # Show the filtered image
    filtered_image = apply_filter(filename)
    filtered_image.show()

def get_file():
    # Read image file path from user, or use the default file
    filename = input('Enter the path to an image file (or press enter to use default image): ')
    if filename == '':
        filename = DEFAULT_FILE
    return filename

def apply_filter(filename):
    """
    Applies a filter reminiscent of Apple II monochrome graphics by:
    1. Scaling the image down to fit into the Apple II double high resolution size of 560x192 pixels, which produces
       a skewed image that looks half as tall as it should. This is done because it is supposedly the actual amount
       of detail on the screen, and presumably the image is then stretched to twice its height to fill the display.
       To emulate this, the image is stretched during a resize in step #3.
    2. The image is made monochrome by turning pixels darker than a threshold a very dark green and pixels lighter than
       a threshold a bright green.
    3. The image is scaled up by 1.5 times, to prepare for simulating scanlines on every third row of pixels. At the
       same time, the skew from earlier is corrected so that the image appears to have the correct aspect ratio.
    4. Every third row of pixels is replaced with dark green to simulate scanlines.
    5. The image is scaled up again to around 20 times the size of the Apple II resolution, for viewing full screen
       on high resolution displays.
    """
    # Create new image
    image = Image.open(filename)
    # Simulate actual Apple II screen resolution of 560x192 pixels
    image = scale_image(image, APPLE_II_WIDTH_ACTUAL, APPLE_II_HEIGHT_PERCEIVED, 1, 2)
    # Make image monochrome green to simulate Apple II monitor appearance
    image = make_monochrome(image)
    # Simulate perceived (non-skewed) Apple II screen resolution (1 "pixel" = 2px tall) and scale up before adding pixel borders
    image = scale_image(image, APPLE_II_WIDTH_ACTUAL * 1.5, APPLE_II_HEIGHT_ACTUAL * 1.5, 1, .5)
    # add_nameplate()  -- not essential, try after everything else is working
    simulate_scanlines(image)
    # Scale image up to size big enough to cover a 4K display
    image = scale_image(image, APPLE_II_WIDTH_ACTUAL * 20, APPLE_II_HEIGHT_ACTUAL * 20, 1, 1)
    return image

def scale_image(image, target_width, target_height, skew_ratio_width, skew_ratio_height):
    """
    Determines what scale factor to use based on comparison of origin image size to target image size, then uses
    Pillow's resize() function to resize based on that scale factor.

    Provides optional parameters for skewing width and height. If constrained aspect ratio is desired, set these to 1.
    """
    scale_factor = get_scale_factor(image.width, image.height, target_width, target_height)  # Get scale factor
    scaled_width = int((image.width / scale_factor) / skew_ratio_width)  # Get scaled width by dividing image width by scale factor, diving that by skew ratio if desired, and turning result into integer for resizing
    scaled_height = int((image.height / scale_factor) / skew_ratio_height)  # Get scaled height by dividing image height by scale factor, diving that by skew ratio if desired, and turning result into integer for resizing
    image = image.resize((scaled_width, scaled_height), resample=4)  # Uses Pillow's resize() function to resize the image to the scaled width and height; uses box resampling to keep pixel borders crisp
    return image

def get_scale_factor(original_width, original_height, target_width, target_height):
    """
    Determines the scale factor for a scaling operation by dividing the original image's dimensions by the target
    dimensions, then comparing width scale to height scale to determine which is larger. This determines which
    dimension we need to use as scale factor so that no part of the image is cropped when the image is scaled to within
    the target dimensions.
    """
    width_ratio = original_width / target_width
    height_ratio = original_height / target_height

    if (original_width == target_width) and (original_height == target_height):
        return 1
    elif width_ratio > height_ratio:  # If width scale is greater than height scale…
        # Use width scale as scale factor
        return width_ratio
    else:
        # Use height scale as scale factor
        return height_ratio

def make_monochrome(image):
    """
    Checks the brightness of each pixel in the image, and sets pixels above a threshold to bright green and below the threshold to very dark green.
    """
    for x in range(image.width):  # For every column of pixels…
        for y in range(image.height):  # For every pixel on each row of the column…
            color = image.getpixel((x,y))  # Get the RGB values of the pixel as a tuple
            brightness_average = (color[0] + color[1] + color[2]) // 3  # Calculate average brightness of pixel; gets RGB values from indices of tuple
            if brightness_average > 105: # If a pixel's brightness average is greater than 105…
                image.putpixel((x,y), MONOCHROME_POSITIVE_TUPLE)  # Draw a pixel at these coordinates of color MONOCHROME_POSITIVE_TUPLE

            else:
                image.putpixel((x, y), MONOCHROME_NEGATIVE_TUPLE)  # Draw a pixel at these coordinates of color MONOCHROME_NEGATIVE_TUPLE
    return image

def simulate_scanlines(image):
    """
    Replace every fourth row of pixels with dark green
    """
    for y in range(image.height):  # For every row of pixels…
        if y % 3 == 0:  # If the row number divides evenly by 3…
            for x in range(image.width):  # For every pixel on each column of the row…
                image.putpixel((x, y), MONOCHROME_NEGATIVE_TUPLE)  # Draw a pixel at these coordinates of color MONOCHROME_NEGATIVE_TUPLE

if __name__ == '__main__':
    main()
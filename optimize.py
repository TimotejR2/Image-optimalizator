import os
import sys
from PIL import Image

SUPPORTED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']

def main():
    if len(sys.argv) not in [1,2,4,5]:
        sys.exit("Usage: python3 optimize.py [<directory>] [<max_width>] [<max_height>] [<suffix>] [<min_resolution>]")
    
    # Default values
    min_resolution = 270
    max_height = 300
    max_width = 500
    suffix = "_low"
    folder = 'images'

    # Get command line arguments
    if len(sys.argv) >= 2:
        folder = sys.argv[1]

    if len(sys.argv) >= 4:
        max_width = int(sys.argv[2])
        max_height = int(sys.argv[3])

    if len(sys.argv) >= 5:
        suffix = sys.argv[4]
    
    if len(sys.argv) == 6:
        min_resolution = int(sys.argv[5])

    # Check if folder exists
    if not os.path.isdir(folder):
        sys.exit("Not a directory")
    
    # Optimize images
    for file in os.listdir(folder):
        if file.endswith(tuple(SUPPORTED_EXTENSIONS)) and file.count('.') == 1:
            image_path = os.path.join(folder, file)
            resize_image(image_path, max_width, max_height, suffix, min_resolution)


def resize_image(image_path, max_width, max_height, suffix, min_resolution):
    """Resizes an image to fit within a given width and height."""

    # Load the original image
    try:
        original_image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Could not find image: {image_path}")
        return
    except OSError:
        print(f"Could not open image: {image_path}")
        return
        
    if suffix in image_path:
        new_filename = image_path
    else:
        new_filename = os.path.splitext(image_path)[0] + suffix + os.path.splitext(image_path)[1]
    print(new_filename)

    # Calculate the new width and height
    width, height = original_image.size
    if height > max_height or width > max_width:
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        new_resolution = (new_width, new_height)

        # Make sure that image isnt too small
        while min(new_resolution) <= min_resolution:
            new_resolution = (int(new_resolution[0] * 1.1), int(new_resolution[1] * 1.1))
            
        print(f"Resizing {image_path} from {width}x{height} to {new_width}x{new_height}")

        # Resize the image
        resized_image = original_image.resize(new_resolution)

        # Save the resized image
        resized_image.save(new_filename)
    else:
        print(f"Not resizing {image_path}")
        original_image.save(new_filename)


if __name__ == "__main__":
    main()

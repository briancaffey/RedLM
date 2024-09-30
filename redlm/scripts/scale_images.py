"""
Test script to figure out the scale factor for reducing image size
"""

import os
from PIL import Image


def scale_image(input_path, output_path, scale_factor=3):
    """
    Scale down original images
    """
    # Open the image file
    with Image.open(input_path) as img:
        # Calculate the new dimensions
        new_width = img.width // scale_factor
        new_height = img.height // scale_factor

        # Resize the image using LANCZOS for high-quality downscaling
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save the resized image
        img_resized.save(output_path, optimize=True)

        print(f"Image saved to {output_path}")


if __name__ == "__main__":
    input_directory = "/home/brian/Documents/hlm/cropped"
    # Ensure the directory exists
    if not os.path.exists(input_directory):
        print(f"Directory {input_directory} does not exist.")
    else:
        # Iterate over all files in the directory
        for filename in os.listdir(input_directory):
            # Check if the file is an image and is not a directory (avoiding '.' and '..')
            if filename.lower().endswith((".png")) and not filename.startswith("."):
                # Input file path
                input_file_path = os.path.join(input_directory, filename)

                # Output file path with a different extension to avoid overwriting the original
                output_file_path = os.path.join(
                    "/home/brian/github/HLLM/hllm/data/paintings", filename
                )

                # Call the scaling function
                scale_image(input_file_path, output_file_path)

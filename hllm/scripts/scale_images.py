"""
Test script to figure out the scale factor for reducing image size
"""

from PIL import Image

def scale_image(input_path, output_path, scale_factor=3):
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
    # TODO convert all images in the directory and save to data dir
    input_image_path = "/home/brian/github/HLLM/hllm/data/paintings/002.png"
    output_image_path = "/home/brian/github/HLLM/hllm/data/paintings/002_scaled.png"

    scale_image(input_image_path, output_image_path)

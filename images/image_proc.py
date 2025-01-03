import argparse
import cv2
import numpy as np


parser = argparse.ArgumentParser(description='Clean background from image')
parser.add_argument('input', type=str, help='Input image')

args = parser.parse_args()

img = cv2.imread(args.input)

# Convert image to RGBA
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# # Define white color range
# lower_white = np.array([200, 200, 200, 255], dtype=np.uint8)
# upper_white = np.array([255, 255, 255, 255], dtype=np.uint8)

# Define black color range
# lower_white = np.array([0, 0, 0, 255], dtype=np.uint8)
# upper_white = np.array([100, 100, 100, 255], dtype=np.uint8)

# Create mask to detect white regions
# mask = cv2.inRange(img, lower_white, upper_white)

# Set alpha channel to 0 for white regions
# img[mask == 255, 3] = 0


# blend left side and right side into transparent
height, width, _ = img.shape

# Create a gradient mask for blending
blend_width = width // 16
gradient = np.linspace(0, 1, blend_width)
gradient = np.tile(gradient, (height, 1))

# Apply gradient to the left side
img[:, :blend_width, 3] = (img[:, :blend_width, 3].astype(float) * gradient).astype(np.uint8)

# Apply gradient to the right side
img[:, -blend_width:, 3] = (img[:, -blend_width:, 3].astype(float) * gradient[:, ::-1]).astype(np.uint8)



# Save the result
output_path = args.input
cv2.imwrite(output_path, img)

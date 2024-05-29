import cv2
import numpy as np
import os
import math

# max_length is 12 m ==> convert it to cm ==> get the number of pixels = length in cm / 4 (the pixel size)
max_length = 12 * 100 / 4
# Function to draw a filled circle at given (x, y) with radius r
def draw_filled_circle(image, x, y, r):
    cv2.circle(image, (int(x), int(y)), int(r), color=(0, 0, 255), thickness=cv2.FILLED)

# Function to draw a line at given angle and length, stopping before hitting a black pixel
def draw_beams(image, x, y, angle, max_length):
    length = 0
    # Loop until the max length of line in pixels
    while length <= max_length:
        # Get the new x = x + length * cos(theta)
        x_curr = int(x + length * math.cos(angle))
        # Get the new y = y + length * sin(theta)
        y_curr = int(y + length * math.sin(angle))

        # Check if the current point is within the image boundaries
        if 0 <= x_curr < image.shape[1] and 0 <= y_curr < image.shape[0]:
            # Check if the pixel at the current point is black
            pixel_value = image[y_curr, x_curr]
            if np.all(pixel_value == 0):
                break
        else:
            # The current point is beyond the image boundaries
            break
        # Increment length of the line until a border of a wall
        length += 1

    # Draw the line up to the last non-black pixel or the image border
    if length > 0:
        x_end = int(x + (length - 1) * math.cos(angle))
        y_end = int(y + (length - 1) * math.sin(angle))
        cv2.line(image, (int(x), int(y)), (x_end, y_end), color=(0, 255, 0), thickness=1)

# Function to convert degrees to radians
def degrees_to_radians(degrees):
    return math.radians(degrees)

# Get user input for x, y, and theta
x = float(input("Enter x-coordinate: "))
y = float(input("Enter y-coordinate: "))
theta = float(input("Enter initial angle (theta):"))

# Get the path to the current script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the image file name
image_filename = "Map.jpg"  # Replace with your image file name

# Construct the full path to the image
image_path = os.path.join(script_directory, image_filename)

# Read the image using OpenCV
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
image_draw = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# Draw the line at the specified location in green, stopping when hitting a black pixel
draw_beams(image_draw, x, y, degrees_to_radians(theta), max_length)

# Loop over angles from theta - 125 to theta + 125 with step 2 degrees
for angle in range(int(theta - 125), int(theta + 126), 2):
    # Convert angle to radians
    angle_rad = degrees_to_radians(angle)

    # Draw a line in green with 12, length, stopping when hitting a black pixel
    draw_beams(image_draw, x, y, angle_rad, max_length)

# Draw the filled circle at the specified location in red
draw_filled_circle(image_draw, x, y, 4)
# Save the modified image
output_path = os.path.join(script_directory, "output_image.jpg")
cv2.imwrite(output_path, image_draw)

# Show the modified image
cv2.imshow("laser-range measurements", image_draw)
cv2.waitKey(0)
cv2.destroyAllWindows()

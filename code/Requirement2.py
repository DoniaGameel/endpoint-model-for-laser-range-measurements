import os
import math
import sys
import cv2
import numpy as np

def endpoint_model(sigma, max_range):
    max_range_in_pixels = max_range * 100 / 4  # Convert to pixels

    # Read the image
    # Get the path to the current script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Specify the image file name
    image_filename = "Map.jpg" 
    # Construct the full path to the image
    image_path = os.path.join(script_directory, image_filename)
    # Read the image using OpenCV
    original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Convert the image to binary
    _, binary_image = cv2.threshold(original_image, 127, 255, cv2.THRESH_BINARY)

    # Apply distance transform
    distance_transform = cv2.distanceTransform(binary_image, cv2.DIST_L2, 3)

    # Calculate likelihood
    likelihood = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((distance_transform)**2) / (sigma**2))
    
    # Normalize the likelihood to the range [0, 1]
    cv2.normalize(likelihood, likelihood, 0, 1.0, cv2.NORM_MINMAX)
    
    # Specify the output image file name for the likelihood at this sigma
    output_filename = f"Likelihood at sigma = {sigma}.png"
    # Construct the full path to the image
    output_path_with_filename = os.path.join(script_directory, output_filename)
    # Save the image using OpenCV
    cv2.imwrite(output_path_with_filename, likelihood * 255)
    
    # Create map_likelihood with the same shape as likelihood
    map_likelihood = np.zeros_like(likelihood)
    # Loop on each 2D-cell of the x,y-grid of the map
    for x in range(0, likelihood.shape[1]):
        for y in range(0, likelihood.shape[0]):
            # Array to save all likelihood at all theta to get the maximum
            likelihood_over_theta = []
            # For all theta
            for theta in range(360):
                # Conbert theta to rad 
                theta_rad = math.radians(theta)
                # 1 to multiply by it
                theta_likelihood = 1
                # Get the end point
                x_end = round(x + max_range_in_pixels * math.cos(theta_rad))
                y_end = round(y + max_range_in_pixels * math.sin(theta_rad))
                # Check the end point isn't outside the boundaries
                if (
                    x_end < 0
                    or x_end >= likelihood.shape[1]
                    or y_end < 0
                    or y_end >= likelihood.shape[0]
                ):
                    # Multiply by small number 
                    theta_likelihood *= sys.float_info.min
                else:
                    # MUltiply by its likelihood
                    theta_likelihood *= likelihood[y_end, x_end]
                likelihood_over_theta.append(theta_likelihood)
            # Get the highest likelihood of all orientations θ as gray value.
            map_likelihood[y, x] = np.max(likelihood_over_theta)
    
    # Save the image to the specified output path
    # Specify the output image file name for the likelihood at this sigma
    output_filename = f"max_range = {max_range}m , sigma = {sigma}.png"
    # Construct the full path to the image
    output_path_with_filename = os.path.join(script_directory, output_filename)
    # Save the image using OpenCV
    cv2.imwrite(output_path_with_filename, map_likelihood * 255)



endpoint_model(sigma=10.0, max_range=3.0)
endpoint_model(sigma=1.0, max_range=0.2)
endpoint_model(sigma=5.0, max_range=0.2)
endpoint_model(sigma=20.0, max_range=0.2)
endpoint_model(sigma=10.0, max_range=0.2)

endpoint_model(sigma=1.0, max_range=0.5)
endpoint_model(sigma=5.0, max_range=0.5)
endpoint_model(sigma=10.0, max_range=0.5)
endpoint_model(sigma=20.0, max_range=0.5)

endpoint_model(sigma=1.0, max_range=1.0)
endpoint_model(sigma=5.0, max_range=1.0)
endpoint_model(sigma=10.0, max_range=1.0)
endpoint_model(sigma=20.0, max_range=1.0)

endpoint_model(sigma=1.0, max_range=2.0)
endpoint_model(sigma=5.0, max_range=2.0)
endpoint_model(sigma=10.0, max_range=2.0)
endpoint_model(sigma=20.0, max_range=2.0)

endpoint_model(sigma=1.0, max_range=3.0)
endpoint_model(sigma=5.0, max_range=3.0)
endpoint_model(sigma=10.0, max_range=3.0)
endpoint_model(sigma=20.0, max_range=3.0)
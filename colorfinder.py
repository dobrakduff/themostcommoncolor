from PIL import Image
import numpy as np
from collections import Counter
from sklearn.cluster import KMeans

def most_common_colors(image, num_colors=3, min_distance=50):
    # Convert image to RGB
    image = image.convert('RGB')

    # Resize image to speed up processing
    image = image.resize((100, 100))

    # Convert image to numpy array
    img_array = np.array(image)

    # Reshape array to 2D (flatten)
    flattened_img_array = img_array.reshape(-1, 3)

    # Apply KMeans clustering to find dominant colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(flattened_img_array)
    dominant_colors = kmeans.cluster_centers_.astype(int)

    # Filter out similar colors
    filtered_colors = []
    for color in dominant_colors:
        if all(np.linalg.norm(color - existing_color) > min_distance for existing_color in filtered_colors):
            filtered_colors.append(color)

    return filtered_colors[:num_colors]

def rgb_to_hex(rgb):
    # Convert RGB tuple to hexadecimal color
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

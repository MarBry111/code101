import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_3d_coordinates(coordinates=None, fill_between=None):
    """
    Plot cubes at specified 3D coordinates or fill space between two points.
    
    Parameters:
    coordinates (list of tuples, optional): List of (x, y, z) integer coordinates
    fill_between (tuple of tuples, optional): Tuple of (start_coord, end_coord) to fill space
    """
    # Create figure and 3D axis
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Set the plot limits
    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    ax.set_zlim(-7, 7)
    
    # Set labels
    ax.set_xlabel('X (Left-Right)')
    ax.set_zlabel('Y (Up-Down)')
    ax.set_ylabel('Z (Front-Back)')
    ax.set_title('3D Coordinate Cube Visualization')
    
    # List to store all coordinates to plot
    coords_to_plot = []
    
    # Handle individual coordinates
    if coordinates:
        coords_to_plot.extend(coordinates)
    
    # Handle fill between option
    if fill_between:
        for fb in fill_between:
            # Unpack start and end coordinates
            start, end = fb
            
            # Validate coordinate ranges
            if not all(-7 <= coord <= 7 for coord in start + end):
                print(f"Warning: Fill coordinates {start} to {end} are outside the -7 to 7 grid.")
                return
            
            # Generate all coordinates between start and end
            x_range = range(min(start[0], end[0]), max(start[0], end[0]) + 1)
            z_range = range(min(start[1], end[1]), max(start[1], end[1]) + 1)
            y_range = range(min(start[2], end[2]), max(start[2], end[2]) + 1)
            
            # Create list of all coordinates in the range
            fill_coords = list(itertools.product(x_range, z_range, y_range))
            coords_to_plot.extend(fill_coords)
        
    # Plot each coordinate as a cube
    for x, y, z in coords_to_plot:
        # Create cube vertices
        cube_vertices = [
            [x, z, y],
            [x+1, z, y],
            [x+1, z+1, y],
            [x, z+1, y],
            [x, z, y+1],
            [x+1, z, y+1],
            [x+1, z+1, y+1],
            [x, z+1, y+1]
        ]
        
        # Define cube faces
        faces = [
            [cube_vertices[0], cube_vertices[1], cube_vertices[2], cube_vertices[3]],  # bottom
            [cube_vertices[4], cube_vertices[5], cube_vertices[6], cube_vertices[7]],  # top
            [cube_vertices[0], cube_vertices[1], cube_vertices[5], cube_vertices[4]],  # front
            [cube_vertices[2], cube_vertices[3], cube_vertices[7], cube_vertices[6]],  # back
            [cube_vertices[1], cube_vertices[2], cube_vertices[6], cube_vertices[5]],  # right
            [cube_vertices[0], cube_vertices[3], cube_vertices[7], cube_vertices[4]]   # left
        ]
        
        # Plot the cube with some transparency
        cube = Poly3DCollection(faces, alpha=0.5, facecolors='cyan', edgecolors='black')
        ax.add_collection3d(cube)
    
    # Adjust the view
    ax.view_init(elev=20, azim=45)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# Example usage
def main():
    # Scenario 1: Specific coordinates
    specific_coords = [
        (0, 0, 0),   # Center cube
        (1, 2, 3),   # Another cube
        (-2, -1, 4)  # Negative coordinates
    ]
    
    fill_coords = [
        [(-5, 0, -5), (5, 0, 5)],
        [(-5, 0, -5), (-5, 5, -5)]
    ]
    
    plot_3d_coordinates(coordinates=specific_coords, fill_between=fill_coords)

# Allow the script to be run directly or imported
if __name__ == "__main__":
    main()
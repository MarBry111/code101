import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys

class CoordinatePlotterApp:
    def __init__(self, master):
        self.master = master
        master.title("3D Coordinate Plotter")
        master.geometry("800x600")

        # Ensure application closes completely when main window is closed
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create main frames
        self.input_frame = ttk.Frame(master, padding="10")
        self.input_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.list_frame = ttk.Frame(master, padding="10")
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Coordinate Input Section
        ttk.Label(self.input_frame, text="Specific Coordinates").pack()
        
        # Coordinate Input Fields
        coord_input_frame = ttk.Frame(self.input_frame)
        coord_input_frame.pack()
        
        ttk.Label(coord_input_frame, text="X:").grid(row=0, column=0)
        self.x_entry = ttk.Entry(coord_input_frame, width=5)
        self.x_entry.grid(row=0, column=1)
        
        ttk.Label(coord_input_frame, text="Y:").grid(row=0, column=2)
        self.y_entry = ttk.Entry(coord_input_frame, width=5)
        self.y_entry.grid(row=0, column=3)
        
        ttk.Label(coord_input_frame, text="Z:").grid(row=0, column=4)
        self.z_entry = ttk.Entry(coord_input_frame, width=5)
        self.z_entry.grid(row=0, column=5)
        
        # Add Coordinate Button
        ttk.Button(self.input_frame, text="Add Coordinate", command=self.add_coordinate).pack()
        
        # Specific Coordinates Listbox
        self.coord_listbox = tk.Listbox(self.list_frame, width=30)
        self.coord_listbox.pack(side=tk.TOP, fill=tk.X)
        
        # Remove Coordinate Button
        ttk.Button(self.list_frame, text="Remove Selected Coordinate", 
                   command=self.remove_coordinate).pack()

        # Fill Region Input Section
        ttk.Label(self.input_frame, text="\nFill Region").pack()
        
        # Fill Region Input Fields
        fill_input_frame = ttk.Frame(self.input_frame)
        fill_input_frame.pack()
        
        ttk.Label(fill_input_frame, text="Start X:").grid(row=0, column=0)
        self.fill_start_x = ttk.Entry(fill_input_frame, width=5)
        self.fill_start_x.grid(row=0, column=1)
        
        ttk.Label(fill_input_frame, text="Start Y:").grid(row=0, column=2)
        self.fill_start_y = ttk.Entry(fill_input_frame, width=5)
        self.fill_start_y.grid(row=0, column=3)
        
        ttk.Label(fill_input_frame, text="Start Z:").grid(row=0, column=4)
        self.fill_start_z = ttk.Entry(fill_input_frame, width=5)
        self.fill_start_z.grid(row=0, column=5)
        
        # End Fill Region Inputs
        ttk.Label(fill_input_frame, text="End X:").grid(row=1, column=0)
        self.fill_end_x = ttk.Entry(fill_input_frame, width=5)
        self.fill_end_x.grid(row=1, column=1)
        
        ttk.Label(fill_input_frame, text="End Y:").grid(row=1, column=2)
        self.fill_end_y = ttk.Entry(fill_input_frame, width=5)
        self.fill_end_y.grid(row=1, column=3)
        
        ttk.Label(fill_input_frame, text="End Z:").grid(row=1, column=4)
        self.fill_end_z = ttk.Entry(fill_input_frame, width=5)
        self.fill_end_z.grid(row=1, column=5)
        
        # Add Fill Region Button
        ttk.Button(self.input_frame, text="Add Fill Region", command=self.add_fill_region).pack()
        
        # Fill Regions Listbox
        self.fill_listbox = tk.Listbox(self.list_frame, width=30)
        self.fill_listbox.pack(side=tk.TOP, fill=tk.X)
        
        # Remove Fill Region Button
        ttk.Button(self.list_frame, text="Remove Selected Fill Region", 
                   command=self.remove_fill_region).pack()

        # Draw Button
        ttk.Button(self.input_frame, text="Draw Plot", command=self.draw_plot).pack(pady=10)

        # Lists to store coordinates and fill regions
        self.coordinates = []
        self.fill_regions = []
        
        # Keep track of plot windows
        self.plot_windows = []

    def on_closing(self):
        """
        Handle closing of the main window.
        Closes all plot windows and the main application.
        """
        # Close all plot windows
        for window in self.plot_windows:
            try:
                window.destroy()
            except:
                pass
        
        # Close matplotlib figures to prevent memory leaks
        plt.close('all')
        
        # Destroy the main window and exit the application
        self.master.destroy()
        sys.exit(0)

    def draw_plot(self):
        # Check if there are any coordinates or fill regions to plot
        if not self.coordinates and not self.fill_regions:
            messagebox.showerror("Error", "Please add coordinates or fill regions")
            return
        
        # Create a new window for the plot
        plot_window = tk.Toplevel(self.master)
        plot_window.title("3D Coordinate Plot")
        
        # Add this window to our list of plot windows
        self.plot_windows.append(plot_window)
        
        # Ensure this plot window also closes properly
        plot_window.protocol("WM_DELETE_WINDOW", lambda: self.close_plot_window(plot_window))
        
        # Create the plot
        fig = self.plot_3d_coordinates(
            coordinates=self.coordinates, 
            fill_between=self.fill_regions
        )
        
        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def close_plot_window(self, window):
        """
        Handle closing of individual plot windows.
        """
        # Remove the window from our tracked windows
        if window in self.plot_windows:
            self.plot_windows.remove(window)
        
        # Close the matplotlib figure to prevent memory leaks
        plt.close(window.winfo_children()[0].figure)
        
        # Destroy the window
        window.destroy()

    def add_coordinate(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            z = int(self.z_entry.get())
            
            # Validate coordinate ranges
            if not all(-7 <= coord <= 7 for coord in (x, y, z)):
                messagebox.showerror("Error", "Coordinates must be between -7 and 7")
                return
            
            coord = (x, y, z)
            self.coordinates.append(coord)
            self.coord_listbox.insert(tk.END, f"({x}, {y}, {z})")
            
            # Clear entries
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
            self.z_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer coordinates")

    def remove_coordinate(self):
        try:
            index = self.coord_listbox.curselection()[0]
            self.coord_listbox.delete(index)
            del self.coordinates[index]
        except IndexError:
            messagebox.showerror("Error", "Please select a coordinate to remove")

    def add_fill_region(self):
        try:
            start_x = int(self.fill_start_x.get())
            start_y = int(self.fill_start_y.get())
            start_z = int(self.fill_start_z.get())
            
            end_x = int(self.fill_end_x.get())
            end_y = int(self.fill_end_y.get())
            end_z = int(self.fill_end_z.get())
            
            # Validate coordinate ranges
            start = (start_x, start_y, start_z)
            end = (end_x, end_y, end_z)
            
            if not all(-7 <= coord <= 7 for coord in start + end):
                messagebox.showerror("Error", "Fill coordinates must be between -7 and 7")
                return
            
            fill_region = (start, end)
            self.fill_regions.append(fill_region)
            self.fill_listbox.insert(tk.END, f"({start_x},{start_y},{start_z}) to ({end_x},{end_y},{end_z})")
            
            # Clear entries
            for entry in [self.fill_start_x, self.fill_start_y, self.fill_start_z,
                          self.fill_end_x, self.fill_end_y, self.fill_end_z]:
                entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer coordinates")

    def remove_fill_region(self):
        try:
            index = self.fill_listbox.curselection()[0]
            self.fill_listbox.delete(index)
            del self.fill_regions[index]
        except IndexError:
            messagebox.showerror("Error", "Please select a fill region to remove")

    def plot_3d_coordinates(self, coordinates=None, fill_between=None):
        """
        Plot cubes at specified 3D coordinates or fill space between two points.
        
        Parameters:
        coordinates (list of tuples, optional): List of (x, y, z) integer coordinates
        fill_between (list of tuples, optional): List of (start_coord, end_coord) to fill space
        """
        # Create figure and 3D axis
        fig = plt.figure(figsize=(10, 8))
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
        
        return fig

    def draw_plot(self):
        # Check if there are any coordinates or fill regions to plot
        if not self.coordinates and not self.fill_regions:
            messagebox.showerror("Error", "Please add coordinates or fill regions")
            return
        
        # Create a new window for the plot
        plot_window = tk.Toplevel(self.master)
        plot_window.title("3D Coordinate Plot")
        
        # Create the plot
        fig = self.plot_3d_coordinates(
            coordinates=self.coordinates, 
            fill_between=self.fill_regions
        )
        
        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = CoordinatePlotterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()



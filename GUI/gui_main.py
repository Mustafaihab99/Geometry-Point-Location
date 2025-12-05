import tkinter as tk
from tkinter import ttk, messagebox
import colorsys
import math

from GeometryFunctions.distance import distance
from GeometryFunctions.ensureCCW import ensure_ccw
from GeometryFunctions.isConvex import is_convex
from GeometryFunctions.pointToLineDistance import point_to_line_distance
from GeometryFunctions.pointInConvexPolygon import point_in_convex_polygon
from RadialStructure.BuildRadialStructure import build_radial_structure
from RadialStructure.findPolygonWithSteps import find_polygon_with_steps
from GeometryFunctions.angle import angle

class PolygonSubdivisionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Polygon Subdivision Point Location - Enhanced")
        self.root.geometry("1600x1000")
        
        # Start with two default polygons
        self.polygons = [
            [(100, 100), (300, 80), (350, 200), (250, 320), (100, 280)],
            [(400, 150), (550, 120), (600, 280), (450, 300)]
        ]
        
        # Algorithm data
        self.center = None
        self.angles = None
        self.sectors = None
        self.processed_polygons = None
        
        # UI state
        self.test_points = []
        self.dragging_point = None
        self.hover_point = None
        self.animation_running = False
        self.animation_speed = 500  # milliseconds per step
        self.search_steps = []
        self.current_step = 0
        
        # Polygon creation state
        self.creating_polygon = False
        self.current_polygon_points = []
        
        # Polygon editing state
        self.editing_polygon = False
        self.editing_polygon_index = -1
        self.selected_vertex = None  # (polygon_index, vertex_index)
        self.dragging_vertex = None
        self.dragging_entire_polygon = False
        self.polygon_drag_offset = (0, 0)
        
        # Colors
        self.polygon_colors = self._generate_colors(20)  # Generate enough colors
        
        # Canvas items for performance
        self.canvas_items = {}
        
        self._setup_ui()
        self._rebuild_structure()
        self._draw_static()
        self._update_info()
        
    def _generate_colors(self, n):
        """Generate distinct colors for polygons."""
        colors = []
        for i in range(n):
            hue = i / n
            rgb = colorsys.hsv_to_rgb(hue, 0.6, 0.9)
            hex_color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            colors.append(hex_color)
        return colors
    
    def _blend_color(self, color1, color2, ratio):
        """Blend two colors."""
        # Convert hex to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB to hex
        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        blended = tuple(int(rgb1[i] * (1 - ratio) + rgb2[i] * ratio) for i in range(3))
        return rgb_to_hex(blended)
    
    def _rebuild_structure(self):
        """Rebuild radial structure from current polygons."""
        if len(self.polygons) < 1:
            self.center = None
            self.angles = []
            self.sectors = []
            self.processed_polygons = []
            return
        
        self.center, self.angles, self.sectors, self.processed_polygons = \
            build_radial_structure(self.polygons)
        self._update_polygon_list()
    
    def _update_polygon_list(self):
        """Update polygon list."""
        self.polygon_listbox.delete(0, tk.END)
        for i, poly in enumerate(self.polygons):
            convex_status = "✓" if is_convex(poly) else "✗"
            self.polygon_listbox.insert(tk.END, f"Polygon {i}: {len(poly)} vertices {convex_status}")
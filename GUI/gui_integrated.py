#  Malak
import tkinter as tk
from tkinter import ttk, messagebox
import colorsys
import math
import random
import time
import threading
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "GeometryFunctions"))
sys.path.insert(0, os.path.join(project_root, "RadialStructure"))
sys.path.insert(0, os.path.join(project_root, "GUI"))

from GeometryFunctions.ensureCCW import ensure_ccw
from GeometryFunctions.isConvex import is_convex
from GeometryFunctions.distance import distance
from GeometryFunctions.pointToLineDistance import point_to_line_distance
from GeometryFunctions.pointInConvexPolygon import point_in_convex_polygon
from GeometryFunctions.angle import angle

from RadialStructure.findPolygonWithSteps import find_polygon_with_steps
from RadialStructure.BuildRadialStructure import build_radial_structure

from GUI.gui_drawing import GUIDrawing
from GUI.gui_events import GUIEvents
from GUI.gui_polygon_management import GUIPolygonManagement
from GUI.gui_animation import GUIAnimation
from GUI.gui_utils import GUIUtils
from GUI.gui_setup import GUISetup


class PolygonSubdivisionGUI(
    GUISetup,
    GUIDrawing,
    GUIEvents,
    GUIPolygonManagement,
    GUIAnimation,
    GUIUtils
):
    def __init__(self, root):
        self.root = root
        self.root.title("Polygon Subdivision Point Location - Enhanced")
        self.root.geometry("1600x1000")
        
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
        self.animation_speed = 500
        self.search_steps = []
        self.current_step = 0
        
        # Polygon creation state
        self.creating_polygon = False
        self.current_polygon_points = []
        
        # Polygon editing state
        self.editing_polygon = False
        self.editing_polygon_index = -1
        self.selected_vertex = None
        self.dragging_vertex = None
        self.dragging_entire_polygon = False
        self.polygon_drag_offset = (0, 0)
        
        # Colors
        self.polygon_colors = self._generate_colors(20)
        
        # Canvas items
        self.canvas_items = {}
        
        # UI elements (سيتم تعريفهم في setup_ui)
        self.polygon_listbox = None
        self.info_text = None
        self.stats_text = None
        self.speed_var = None
        
        # Display options
        self.show_rays_var = None
        self.show_sectors_var = None
        self.show_center_var = None
        self.show_animation_var = None
        self.show_search_range_var = None
        self.highlight_editing_var = None
        
        # Undo stack
        self._previous_polygons = None
        
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
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
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
        if hasattr(self, 'polygon_listbox') and self.polygon_listbox:
            self._update_polygon_list()
    
    def _update_polygon_list(self):
        """Update polygon list."""
        if hasattr(self, 'polygon_listbox'):
            self.polygon_listbox.delete(0, tk.END)
            for i, poly in enumerate(self.polygons):
                convex_status = "✓" if is_convex(poly) else "✗"
                self.polygon_listbox.insert(tk.END, f"Polygon {i}: {len(poly)} vertices {convex_status}")
    
    def redraw_all(self):
        """Redraw everything in correct order."""
        # Clear everything first
        self.canvas.delete('all')
        
        # Draw static elements (polygons first)
        self._draw_static()
        
        # Then draw dynamic elements
        self._draw_dynamic()
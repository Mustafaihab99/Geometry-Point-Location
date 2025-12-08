# Menna
import tkinter as tk
from tkinter import messagebox
import random
import math
from turtle import distance

class GUIPolygonManagement:
    def _start_new_polygon(self):
        """Start creating a new polygon."""
        self._stop_editing()
        self.creating_polygon = True
        self.current_polygon_points = []
        messagebox.showinfo("Create Polygon", 
                          "Right-click to add vertices.\n"
                          "Click 'Finish Polygon' when done (minimum 3 vertices).\n"
                          "Click 'Cancel Creation' to cancel.")
        self._draw_static()
    
    def _finish_polygon(self):
        """Finish creating the current polygon."""
        if not self.creating_polygon:
            messagebox.showwarning("No Polygon", "No polygon is being created.")
            return
        
        if len(self.current_polygon_points) < 3:
            messagebox.showwarning("Too Few Vertices", 
                                 f"Polygon needs at least 3 vertices. You have {len(self.current_polygon_points)}.")
            return
        
        self._previous_polygons = self.polygons.copy()
        
        self.polygons.append(self.current_polygon_points)
        self.creating_polygon = False
        self.current_polygon_points = []
        
        self._rebuild_structure()
        self._draw_static()
        self._draw_dynamic()
        self._update_info()
        
        messagebox.showinfo("Success", f"Polygon added successfully! Total polygons: {len(self.polygons)}")
    
    def _cancel_polygon_creation(self):
        """Cancel current polygon creation."""
        self.creating_polygon = False
        self.current_polygon_points = []
        self._draw_static()
        self._draw_dynamic()
    
    def _start_editing(self):
        """Start editing mode."""
        if not hasattr(self, 'polygon_listbox'):
            return
            
        selection = self.polygon_listbox.curselection()
        if selection:
            self._start_editing_polygon(selection[0])
        else:
            messagebox.showwarning("No Selection", "Please select a polygon to edit.")
    
    def _start_editing_polygon(self, index):
        """Start editing a specific polygon."""
        if index < 0 or index >= len(self.polygons):
            return
        
        self._previous_polygons = self.polygons.copy()
        
        self._stop_editing()
        self.editing_polygon = True
        self.editing_polygon_index = index
        self.selected_vertex = None
        
        if hasattr(self, 'polygon_listbox'):
            self.polygon_listbox.selection_clear(0, tk.END)
            self.polygon_listbox.selection_set(index)
            self.polygon_listbox.see(index)
        
        messagebox.showinfo("Edit Polygon", 
                          f"Now editing Polygon {index}.\n"
                          f"• Drag vertices to move them\n"
                          f"• Click near edge to add vertex\n"
                          f"• Press Delete to remove selected vertex\n"
                          f"• Drag center to move entire polygon\n"
                          f"• Press Escape to stop editing")
        
        self._draw_static()
    
    def _stop_editing(self, event=None):
        """Stop editing mode."""
        self.editing_polygon = False
        self.editing_polygon_index = -1
        self.selected_vertex = None
        self.dragging_vertex = None
        self.dragging_entire_polygon = False
        
        if hasattr(self, 'polygon_listbox'):
            self.polygon_listbox.selection_clear(0, tk.END)
        self._draw_static()
    
    def _add_vertex_to_selected(self):
        """Add vertex to selected polygon at midpoint of selected edge."""
        if not self.editing_polygon or self.editing_polygon_index < 0:
            messagebox.showwarning("No Editing", "Not in editing mode.")
            return
        
        poly = self.polygons[self.editing_polygon_index]
        
        if len(poly) < 2:
            messagebox.showwarning("Too Few Vertices", "Polygon needs at least 2 vertices.")
            return
        
        self._previous_polygons = self.polygons.copy()
        
        max_length = -1
        best_index = -1
        
        for i in range(len(poly)):
            p1 = poly[i]
            p2 = poly[(i + 1) % len(poly)]
            length = distance(p1, p2)
            if length > max_length:
                max_length = length
                best_index = i
        
        if best_index >= 0:
            p1 = poly[best_index]
            p2 = poly[(best_index + 1) % len(poly)]
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            
            self.polygons[self.editing_polygon_index].insert(best_index + 1, (mid_x, mid_y))
            self.selected_vertex = (self.editing_polygon_index, best_index + 1)
            self._rebuild_structure()
            self._draw_static()
            self._draw_dynamic()
    
    def _delete_selected_vertex(self, event=None):
        """Delete the selected vertex."""
        if not self.editing_polygon or self.selected_vertex is None:
            return
        
        poly_idx, vertex_idx = self.selected_vertex
        
        if poly_idx < len(self.polygons) and vertex_idx < len(self.polygons[poly_idx]):
            if len(self.polygons[poly_idx]) <= 3:
                messagebox.showwarning("Cannot Delete", "Polygon must have at least 3 vertices.")
                return
            
            self._previous_polygons = self.polygons.copy()
            
            del self.polygons[poly_idx][vertex_idx]
            self.selected_vertex = None
            
            self._rebuild_structure()
            self._draw_static()
            self._draw_dynamic()
    
    def _add_random_polygon(self):
        """Add a random convex polygon."""
        self._previous_polygons = self.polygons.copy()
        
        center_x = random.randint(200, 800)
        center_y = random.randint(200, 600)
        
        num_vertices = random.randint(3, 7)
        
        angles = sorted([random.uniform(0, 2*math.pi) for _ in range(num_vertices)])
        radii = [random.uniform(50, 150) for _ in range(num_vertices)]
        
        polygon = []
        for i in range(num_vertices):
            x = center_x + radii[i] * math.cos(angles[i])
            y = center_y + radii[i] * math.sin(angles[i])
            polygon.append((x, y))
        
        from GeometryFunctions.ensureCCW import ensure_ccw
        polygon = ensure_ccw(polygon)
        
        self.polygons.append(polygon)
        self._rebuild_structure()
        self._draw_static()
        self._draw_dynamic()
        self._update_info()
        
        messagebox.showinfo("Random Polygon", 
                          f"Random polygon with {num_vertices} vertices added successfully!")
    
    def _clear_all_polygons(self):
        """Clear all polygons."""
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all polygons?"):
            self._previous_polygons = self.polygons.copy()
            
            self.polygons = []
            self.test_points = []
            self.search_steps = []
            self.current_step = 0
            self._stop_editing()
            self._rebuild_structure()
            self._draw_static()
            self._draw_dynamic()
            self._update_info()
            if hasattr(self, '_update_stats'):
                self._update_stats()
    
    def _delete_selected_polygon(self):
        """Delete selected polygon from list."""
        if not hasattr(self, 'polygon_listbox'):
            return
            
        selection = self.polygon_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a polygon to delete.")
            return
        
        index = selection[0]
        if messagebox.askyesno("Delete Polygon", f"Delete polygon {index}?"):
            self._previous_polygons = self.polygons.copy()
            
            self.polygons.pop(index)
            self._stop_editing()
            self._rebuild_structure()
            self._draw_static()
            self._draw_dynamic()
            self._update_info()
    
    def _reorder_polygon(self, direction):
        """Reorder polygon in the list (move up or down)."""
        if not hasattr(self, 'polygon_listbox'):
            return
            
        selection = self.polygon_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        new_index = index + direction
        
        if 0 <= new_index < len(self.polygons):
            self._previous_polygons = self.polygons.copy()
            
            self.polygons[index], self.polygons[new_index] = self.polygons[new_index], self.polygons[index]
            
            self._rebuild_structure()
            self.polygon_listbox.selection_clear(0, tk.END)
            self.polygon_listbox.selection_set(new_index)

            if self.editing_polygon and self.editing_polygon_index == index:
                self.editing_polygon_index = new_index
            elif self.editing_polygon and self.editing_polygon_index == new_index:
                self.editing_polygon_index = index
            
            self._draw_static()
            self._draw_dynamic()
    
    def _undo_last_change(self, event=None):
        """Undo last polygon change."""
        if hasattr(self, '_previous_polygons') and self._previous_polygons:
            self.polygons = self._previous_polygons.copy()
            self._rebuild_structure()
            self._draw_static()
            self._draw_dynamic()
            self._update_info()
# :) NADA :)
from tkinter import messagebox

from GeometryFunctions.distance import distance
from GeometryFunctions.pointInConvexPolygon import point_in_convex_polygon
from GeometryFunctions.pointToLineDistance import point_to_line_distance
from RadialStructure.findPolygonWithSteps import find_polygon_with_steps

class GUIEvents:
    def _on_canvas_click(self, event):
        """Handle left click on canvas."""
        x, y = event.x, event.y
        
        if self.creating_polygon:
            return
        
        if self.editing_polygon and self.editing_polygon_index >= 0:
            poly = self.polygons[self.editing_polygon_index]
            
            for i, (vx, vy) in enumerate(poly):
                if distance((x, y), (vx, vy)) < 10:
                    self.selected_vertex = (self.editing_polygon_index, i)
                    self.dragging_vertex = (self.editing_polygon_index, i)
                    self._draw_static()
                    return
            
            cx = sum(p[0] for p in poly) / len(poly)
            cy = sum(p[1] for p in poly) / len(poly)
            if distance((x, y), (cx, cy)) < 15:
                self.dragging_entire_polygon = True
                self.polygon_drag_offset = (cx - x, cy - y)
                return
            
            for i in range(len(poly)):
                p1 = poly[i]
                p2 = poly[(i + 1) % len(poly)]
                
                if point_to_line_distance((x, y), p1, p2) < 10:
                    self.polygons[self.editing_polygon_index].insert(i + 1, (x, y))
                    self.selected_vertex = (self.editing_polygon_index, i + 1)
                    self._rebuild_structure()
                    self._draw_static()
                    self._draw_dynamic()
                    return
        
        for point, _ in self.test_points:
            px, py = point
            if abs(px - x) < 8 and abs(py - y) < 8:
                self.dragging_point = point
                return
        
        point = (x, y)
        result, search_steps = find_polygon_with_steps(
            point, self.center, self.angles, 
            self.sectors, self.processed_polygons,
            self.current_polygon_points if self.creating_polygon else None
        )
        
        self.test_points.append((point, result))
        self.search_steps = search_steps
        self.current_step = 0
        
        if hasattr(self, 'redraw_all'):
            self.redraw_all()
        else:
            self._draw_dynamic()
        self._update_info()
        self._update_stats()
    
    def _on_canvas_double_click(self, event):
        """Handle double click to edit polygon."""
        x, y = event.x, event.y
        
        for i, poly in enumerate(self.processed_polygons):
            if point_in_convex_polygon((x, y), poly):
                self._start_editing_polygon(i)
                return
    
    def _on_canvas_right_click(self, event):
        """Handle right click on canvas to create polygon."""
        if self.creating_polygon:
            x, y = event.x, event.y
            self.current_polygon_points.append((x, y))
            self._draw_static()
            self._draw_dynamic()
    
    def _on_canvas_drag(self, event):
        """Handle dragging."""
        x, y = event.x, event.y
        
        if self.dragging_point:
            for i, (point, result) in enumerate(self.test_points):
                if point == self.dragging_point:
                    new_point = (x, y)
                    
                    new_result, new_steps = find_polygon_with_steps(
                        new_point, self.center, self.angles,
                        self.sectors, self.processed_polygons,
                        self.current_polygon_points if self.creating_polygon else None
                    )
                    
                    self.test_points[i] = (new_point, new_result)
                    self.search_steps = new_steps
                    self.current_step = 0
                    self.dragging_point = new_point
                    
                    self._draw_dynamic()
                    self._update_info()
                    self._update_stats()
                    break
        
        elif self.dragging_vertex:
            poly_idx, vertex_idx = self.dragging_vertex
            if poly_idx < len(self.polygons) and vertex_idx < len(self.polygons[poly_idx]):
                self.polygons[poly_idx][vertex_idx] = (x, y)
                self._rebuild_structure()
                self._draw_static()
                self._draw_dynamic()
        
        elif self.dragging_entire_polygon and self.editing_polygon_index >= 0:
            poly = self.polygons[self.editing_polygon_index]
            dx = x + self.polygon_drag_offset[0]
            dy = y + self.polygon_drag_offset[1]
            
            current_cx = sum(p[0] for p in poly) / len(poly)
            current_cy = sum(p[1] for p in poly) / len(poly)
            
            tx = dx - current_cx
            ty = dy - current_cy
            
            for i in range(len(poly)):
                vx, vy = poly[i]
                poly[i] = (vx + tx, vy + ty)
            
            self._rebuild_structure()
            self._draw_static()
            self._draw_dynamic()
    
    def _on_canvas_release(self, event):
        """Handle button release."""
        self.dragging_point = None
        self.dragging_vertex = None
        self.dragging_entire_polygon = False
    
    def _on_canvas_hover(self, event):
        """Handle mouse hover for highlighting."""
        new_hover_point = None
        
        for point, _ in self.test_points:
            px, py = point
            if abs(px - event.x) < 10 and abs(py - event.y) < 10:
                new_hover_point = point
                break
        
        if new_hover_point != self.hover_point:
            self.hover_point = new_hover_point
            self._draw_dynamic()
    
    def _on_polygon_select(self, event):
        """Handle polygon selection from listbox."""
        selection = self.polygon_listbox.curselection()
        if selection:
            index = selection[0]
            self._start_editing_polygon(index)
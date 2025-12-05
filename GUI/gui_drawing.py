import tkinter as tk
import math
from GeometryFunctions.distance import distance
from GeometryFunctions.pointInConvexPolygon import point_in_convex_polygon
from GeometryFunctions.angle import angle

class GUIDrawing:
    def _draw_static(self):
        """Draw static elements (polygons, center)."""
        # Clear only static elements
        self.canvas.delete('static')
        
        if not self.processed_polygons:
            return
        
        # Draw polygons
        for i, poly in enumerate(self.processed_polygons):
            points = []
            for x, y in poly:
                points.extend([x, y])
            
            color_index = i % len(self.polygon_colors)
            fill_color = self.polygon_colors[color_index]
            outline_color = '#000000'
            outline_width = 2
            
            # Highlight the polygon being edited
            if self.editing_polygon and i == self.editing_polygon_index and self.highlight_editing_var.get():
                fill_color = self._blend_color(fill_color, '#FFFF00', 0.3)
                outline_color = '#FF0000'
                outline_width = 3
            
            self.canvas.create_polygon(points, 
                                      fill=fill_color,
                                      outline=outline_color, 
                                      width=outline_width, 
                                      tags=f'static polygon_{i}')
            
            # Draw vertices with numbers
            for j, (x, y) in enumerate(poly):
                vertex_color = '#000000'
                vertex_size = 4
                
                # Highlight selected vertex
                if self.editing_polygon and i == self.editing_polygon_index and self.selected_vertex == (i, j):
                    vertex_color = '#FF0000'
                    vertex_size = 6
                
                self.canvas.create_oval(x-vertex_size, y-vertex_size, x+vertex_size, y+vertex_size, 
                                       fill=vertex_color, 
                                       outline='white', 
                                       width=1, 
                                       tags=f'static vertex_{i}_{j}')
                self.canvas.create_text(x, y+15, 
                                       text=f'P{i}.{j}', 
                                       fill=vertex_color, 
                                       font=('Arial', 8),
                                       tags='static vertex_label')
            
            # Draw polygon center for dragging
            if self.editing_polygon and i == self.editing_polygon_index:
                # Calculate polygon center
                cx = sum(p[0] for p in poly) / len(poly)
                cy = sum(p[1] for p in poly) / len(poly)
                
                self.canvas.create_oval(cx-8, cy-8, cx+8, cy+8,
                                       fill='#00FF00',
                                       outline='white',
                                       width=2,
                                       tags=f'static polycenter_{i}')
                self.canvas.create_text(cx, cy-20,
                                       text='Drag to move',
                                       fill='#00FF00',
                                       font=('Arial', 8, 'bold'),
                                       tags='static centerlabel_{i}')
        
        # Draw center of radial structure
        if self.show_center_var.get() and self.center:
            cx, cy = self.center
            self.canvas.create_oval(cx-6, cy-6, cx+6, cy+6, 
                                   fill='#FF0000', 
                                   outline='white', 
                                   width=2, 
                                   tags='static center')
            self.canvas.create_text(cx, cy-15, 
                                   text='Center', 
                                   fill='#FF0000', 
                                   font=('Arial', 10, 'bold'),
                                   tags='static center_label')
        
        # Draw polygon being created
        if self.creating_polygon and len(self.current_polygon_points) > 0:
            points = []
            for x, y in self.current_polygon_points:
                points.extend([x, y])
            
            # Draw partial polygon with dashed line
            if len(self.current_polygon_points) > 1:
                self.canvas.create_line(points, 
                                       fill='#FF00FF', 
                                       width=2, 
                                       dash=(4, 2),
                                       tags='static creation_line')
            
            # Draw vertices of polygon being created
            for j, (x, y) in enumerate(self.current_polygon_points):
                self.canvas.create_oval(x-5, y-5, x+5, y+5, 
                                       fill='#FF00FF', 
                                       outline='white', 
                                       width=2, 
                                       tags='static creation_vertex')
                self.canvas.create_text(x, y-15, 
                                       text=f'V{j}', 
                                       fill='#FF00FF', 
                                       font=('Arial', 9, 'bold'),
                                       tags='static creation_label')
    
    def _draw_dynamic(self):
        """Draw dynamic elements (rays, sectors, animation)."""
        # Clear dynamic elements
        self.canvas.delete('dynamic')
        self.canvas.delete('animation')
        
        if not self.center or not self.angles:
            return
        
        cx, cy = self.center
        
        # Draw test points أولاً علشان ميغطوش على المضلعات
        self._draw_test_points()
        
        # Draw angle sectors بعد كدا
        if self.show_sectors_var.get():
            self._draw_sectors()
        
        # Draw angle rays
        if self.show_rays_var.get():
            self._draw_rays()
        
        # Draw binary search animation
        if self.show_animation_var.get() and self.search_steps and self.current_step < len(self.search_steps):
            self._draw_binary_search_animation()
    
    def _draw_sectors(self):
        """Draw angle sectors with colors - lightly."""
        if not self.show_sectors_var.get():
            return  # مترسمش حاجة لو المستخدم مش عاوزها
        
        radius = 500
        cx, cy = self.center
        
        for i in range(len(self.angles)):
            a1 = self.angles[i]
            a2 = self.angles[(i + 1) % len(self.angles)]
            
            if a2 <= a1:
                a2 += 2 * math.pi
            
            face = self.sectors[i] if i < len(self.sectors) else -1
            
            start_deg = math.degrees(a1)
            extent_deg = math.degrees(a2 - a1)
            
            # فقط رسمناهم كدائرة فاتحة
            if face >= 0 and face < len(self.processed_polygons):
                # استخدم 10% opacity فقط
                color_index = face % len(self.polygon_colors)
                color = self.polygon_colors[color_index]
                # خليها فاتحة قوي
                alpha_color = self._blend_color(color, '#FFFFFF', 0.95)
                
                x1, y1 = cx - radius, cy - radius
                x2, y2 = cx + radius, cy + radius
                
                self.canvas.create_arc(x1, y1, x2, y2, 
                                      start=start_deg, extent=extent_deg,
                                      fill=alpha_color, 
                                      outline='',  # من غير outline
                                      width=0,
                                      tags='dynamic sector')
    
    def _draw_rays(self):
        """Draw rays from center through angle points."""
        radius = 600
        cx, cy = self.center
        
        for i, ang in enumerate(self.angles):
            x = cx + radius * math.cos(ang)
            y = cy + radius * math.sin(ang)
            
            self.canvas.create_line(cx, cy, x, y, 
                                   fill='#CCCCCC', width=1, 
                                   dash=(2, 4), tags=f'dynamic ray_{i}')
            
            # Angle labels
            label_x = cx + 350 * math.cos(ang)
            label_y = cy + 350 * math.sin(ang)
            self.canvas.create_text(label_x, label_y, 
                                   text=f'θ{i}', 
                                   fill='#666666', 
                                   font=('Arial', 8),
                                   tags='dynamic angle_label')
    
    def _draw_test_points(self):
        """Draw all test points with results."""
        for point, result in self.test_points:
            x, y = point
            
            if result >= 0 and result < len(self.processed_polygons):
                color_index = result % len(self.polygon_colors)
                color = self.polygon_colors[color_index]
                text = f'P{result}'
            elif result == -2:  # Special case: point is in polygon being created
                color = '#FF00FF'  # Purple/magenta color for creation polygon
                text = 'IN CREATION'
            else:
                color = '#999999'
                text = 'OUT'
            
            outline_color = '#000000'
            outline_width = 2
            
            if self.hover_point == point:
                outline_color = '#FF0000'
                outline_width = 3
            
            point_id = self.canvas.create_oval(x-6, y-6, x+6, y+6, 
                                             fill=color, 
                                             outline=outline_color, 
                                             width=outline_width, 
                                             tags='dynamic test_point')
            
            self.canvas_items[f"point_{x}_{y}"] = point_id
            
            self.canvas.create_text(x, y-20, 
                                   text=text, 
                                   fill='#000000', 
                                   font=('Arial', 9, 'bold'),
                                   tags='dynamic test_label')
            
            if self.center:
                cx, cy = self.center
                self.canvas.create_line(cx, cy, x, y, 
                                    fill=color, width=1, 
                                    dash=(2, 2), tags='dynamic angle_line')
    
    def _draw_binary_search_animation(self):
        """Draw binary search animation with current step."""
        if not self.search_steps or self.current_step >= len(self.search_steps):
            return
        
        if not self.center or not self.angles:
            return
        
        step = self.search_steps[self.current_step]
        cx, cy = self.center
        
        if self.show_search_range_var.get():
            left_idx = step['left']
            right_idx = step['right']
            
            radius = 300
            for i in range(left_idx, right_idx + 1):
                if i < len(self.angles):
                    ang = self.angles[i]
                    x = cx + radius * math.cos(ang)
                    y = cy + radius * math.sin(ang)
                    
                    self.canvas.create_oval(x-8, y-8, x+8, y+8,
                                        fill='#FFFF00', outline='#FF9900',
                                        width=2, tags='animation search_range')
                    
                    self.canvas.create_text(x, y+15, 
                                        text=f'[{i}]', 
                                        fill='#FF9900', 
                                        font=('Arial', 8, 'bold'),
                                        tags='animation range_label')
        
        mid_idx = step['mid']
        if mid_idx < len(self.angles):
            ang_mid = self.angles[mid_idx]
            
            radius = 400
            x_mid = cx + radius * math.cos(ang_mid)
            y_mid = cy + radius * math.sin(ang_mid)
            
            self.canvas.create_line(cx, cy, x_mid, y_mid, 
                                fill='#FF0000', width=3, 
                                arrow=tk.LAST, tags='animation mid_pointer')
            
            self.canvas.create_oval(x_mid-10, y_mid-10, x_mid+10, y_mid+10,
                                fill='#FF0000', outline='white',
                                width=2, tags='animation mid_point')
            
            self.canvas.create_text(x_mid, y_mid-20, 
                                text=f'Mid={mid_idx}\nθ={ang_mid:.2f}', 
                                fill='#FF0000', 
                                font=('Arial', 9, 'bold'),
                                tags='animation mid_label')
        
        radius_target = 450
        x_target = cx + radius_target * math.cos(step['target'])
        y_target = cy + radius_target * math.sin(step['target'])
        
        self.canvas.create_line(cx, cy, x_target, y_target, 
                            fill='#00AA00', width=2, 
                            dash=(3, 3), tags='animation target_line')
        
        self.canvas.create_oval(x_target-8, y_target-8, x_target+8, y_target+8,
                            fill='#00AA00', outline='white',
                            width=2, tags='animation target_point')
        
        decision = "Target ≤ Mid" if step['condition'] else "Target > Mid"
        color = "#00AA00" if step['condition'] else "#FF4444"
        
        self.canvas.create_text(cx, cy-100, 
                            text=f"Step {self.current_step + 1}/{len(self.search_steps)}\n"
                                    f"Decision: {decision}",
                            fill=color, 
                            font=('Arial', 10, 'bold'),
                            tags='animation decision_text')
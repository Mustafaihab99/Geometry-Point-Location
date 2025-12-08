# mustafa & kareem 
import tkinter as tk
from tkinter import messagebox
import math

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "GeometryFunctions"))

from angle import angle
from isConvex import is_convex

class GUIUtils:
    def _update_info(self):
        """Update algorithm information text."""
        self.info_text.delete('1.0', tk.END)
        
        if not self.center or not self.processed_polygons:
            self.info_text.insert(tk.END, "No polygons loaded.")
            return
        
        info = f"╔═══════════════════════════════════════╗\n"
        info += f"║   Radial Structure Information   ║\n"
        info += f"╚═══════════════════════════════════════╝\n\n"
        
        info += f"• Total Polygons: {len(self.polygons)}\n"
        info += f"• Center Point: ({self.center[0]:.1f}, {self.center[1]:.1f})\n"
        info += f"• Number of Angles/Sectors: {len(self.angles)}\n"
        
        if self.creating_polygon:
            info += f"• Creating Polygon: {len(self.current_polygon_points)} vertices\n\n"
        elif self.editing_polygon:
            info += f"• Editing Polygon: {self.editing_polygon_index}\n"
            if self.selected_vertex:
                info += f"• Selected Vertex: {self.selected_vertex[1]}\n\n"
        
        if self.angles:
            info += f"📐 Angle List (first 5):\n"
            for i, ang in enumerate(self.angles[:5]):
                info += f"   θ{i}: {math.degrees(ang):.1f}°\n"
            if len(self.angles) > 5:
                info += f"   ... and {len(self.angles) - 5} more\n"
        
        if self.sectors:
            info += f"\n📊 Sector Assignments (first 5):\n"
            for i, face in enumerate(self.sectors[:5]):
                status = f"→ Polygon {face}" if face >= 0 else "→ Empty"
                info += f"   Sector {i}: {status}\n"
            if len(self.sectors) > 5:
                info += f"   ... and {len(self.sectors) - 5} more\n"
        
        if self.test_points:
            info += f"\n🎯 Last Test Point:\n"
            last_point, last_result = self.test_points[-1]
            if self.center:
                ang = angle(self.center, last_point)
                info += f"   Point: {last_point}\n"
                info += f"   Angle: {math.degrees(ang):.1f}°\n"
            
            if last_result == -2:
                info += f"   Result: IN CREATION POLYGON\n"
            else:
                info += f"   Result: {'Polygon ' + str(last_result) if last_result >= 0 else 'OUT'}\n"
            info += f"   Search Steps: {len(self.search_steps)}\n"
        
        self.info_text.insert(tk.END, info)
    
    def _update_stats(self):
        """Update statistics and animation steps text."""
        self.stats_text.delete('1.0', tk.END)
        
        stats = f"╔══════════════════════════════════╗\n"
        stats += f"║     Statistics & Animation     ║\n"
        stats += f"╚══════════════════════════════════╝\n\n"
        
        # Test statistics
        stats += f"📈 Test Statistics:\n"
        stats += f"   Total Tests: {len(self.test_points)}\n"
        
        counts = {}
        for _, result in self.test_points:
            if result >= 0:
                counts[result] = counts.get(result, 0) + 1
            elif result == -2:
                counts['IN CREATION'] = counts.get('IN CREATION', 0) + 1
            else:
                counts['OUT'] = counts.get('OUT', 0) + 1
        
        for key in sorted(counts.keys()):
            if key == 'OUT':
                stats += f"   OUT: {counts[key]}\n"
            elif key == 'IN CREATION':
                stats += f"   IN CREATION: {counts[key]}\n"
            else:
                stats += f"   Polygon {key}: {counts[key]}\n"
        
        # Polygon statistics
        stats += f"\n📊 Polygon Statistics:\n"
        for i, poly in enumerate(self.polygons):
            convex = "✓" if is_convex(poly) else "✗"
            stats += f"   Polygon {i}: {len(poly)} vertices {convex}\n"
        
        # Animation steps
        if self.search_steps and self.current_step < len(self.search_steps):
            stats += f"\n🔄 Binary Search Steps ({self.current_step + 1}/{len(self.search_steps)}):\n"
            
            step = self.search_steps[self.current_step]
            stats += f"   Current Range: [{step['left']}, {step['right']}]\n"
            stats += f"   Mid Index: {step['mid']}\n"
            stats += f"   Target Angle: {math.degrees(step['target']):.1f}°\n"
            stats += f"   Mid Angle: {math.degrees(step['mid_value']):.1f}°\n"
            
            if step['condition']:
                stats += f"   Decision: Target ≤ Mid → Search Right\n"
            else:
                stats += f"   Decision: Target > Mid → Search Left\n"
            
            # Show all steps
            stats += f"\n📋 All Steps:\n"
            for i, s in enumerate(self.search_steps):
                marker = "▶" if i == self.current_step else " "
                cond = "≤" if s['condition'] else ">"
                stats += f"   {marker} Step {i+1}: [{s['left']}, {s['right']}] "
                stats += f"mid={s['mid']} (target {cond} mid)\n"
        
        self.stats_text.insert(tk.END, stats)
    
    def _load_example(self, num):
        """Load example polygon sets."""
        # Save current state for undo
        self._previous_polygons = self.polygons.copy()
        
        if num == 1:
            self.polygons = [
                [(100, 100), (300, 80), (350, 200), (250, 320), (100, 280)],
                [(400, 150), (550, 120), (600, 280), (450, 300)],
                [(200, 400), (350, 380), (380, 500), (200, 520)]
            ]
        else:
            self.polygons = [
                [(150, 150), (250, 100), (350, 150), (300, 250), (150, 250)],
                [(400, 200), (500, 150), (550, 250), (450, 300)],
                [(200, 350), (300, 320), (350, 400), (280, 480), (180, 450)],
                [(450, 400), (550, 380), (580, 480), (480, 500)]
            ]
        
        self._stop_editing()
        self.creating_polygon = False
        self.current_polygon_points = []
        self.test_points = []
        self.search_steps = []
        self.current_step = 0
        self._rebuild_structure()
        self._draw_static()
        self._draw_dynamic()
        self._update_info()
        self._update_stats()
        
        messagebox.showinfo("Example Loaded", f"Example {num} loaded successfully!")
    
    def _reset_view(self):
        """Reset the view (zoom and pan)."""
        self.canvas.scale("all", 0, 0, 1, 1)
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
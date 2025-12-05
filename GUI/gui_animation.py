import time
import threading
import random
from RadialStructure.findPolygonWithSteps import find_polygon_with_steps

class GUIAnimation:
    def _play_animation(self):
        """Play binary search animation."""
        if not self.search_steps or self.animation_running:
            return
        
        self.animation_running = True
        
        def animate():
            for step in range(len(self.search_steps)):
                if not self.animation_running:
                    break
                
                self.current_step = step
                self._draw_dynamic()
                self._update_stats()
                self.root.update()
                
                time.sleep(self.animation_speed / 1000.0)
            
            self.animation_running = False
        
        thread = threading.Thread(target=animate)
        thread.daemon = True
        thread.start()
    
    def _step_forward(self):
        """Move to next step in animation."""
        if self.search_steps and self.current_step < len(self.search_steps) - 1:
            self.current_step += 1
            self._draw_dynamic()
            self._update_stats()
    
    def _step_back(self):
        """Go back to previous step in animation."""
        if self.current_step > 0:
            self.current_step -= 1
            self._draw_dynamic()
            self._update_stats()
    
    def _reset_animation(self):
        """Reset animation to first step."""
        self.current_step = 0
        self.animation_running = False
        self._draw_dynamic()
        self._update_stats()
    
    def _clear_test_points(self):
        """Clear all test points."""
        self.test_points = []
        self.search_steps = []
        self.current_step = 0
        self._draw_dynamic()
        self._update_info()
        self._update_stats()
    
    def _add_random_point(self):
        """Add a random test point."""
        xs, ys = [], []
        for poly in self.processed_polygons:
            for x, y in poly:
                xs.append(x)
                ys.append(y)
        
        if not xs:  
            min_x, max_x = 0, 1000
            min_y, max_y = 0, 800
        else:
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
        
        x = random.randint(int(min_x) - 50, int(max_x) + 50)
        y = random.randint(int(min_y) - 50, int(max_y) + 50)
        
        point = (x, y)
        result, search_steps = find_polygon_with_steps(
            point, self.center, self.angles, 
            self.sectors, self.processed_polygons,
            self.current_polygon_points if self.creating_polygon else None
        )
        
        self.test_points.append((point, result))
        self.search_steps = search_steps
        self.current_step = 0
        
        self._draw_dynamic()
        self._update_info()
        self._update_stats()
# fadel
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from cross_product import cross_product

def point_in_convex_polygon(point, poly):
    """Check if a point is inside a convex polygon."""
    n = len(poly)
    if n < 3:
        return False
    
    EPSILON = 0.0000001
    first_cross = cross_product(poly[0], poly[1], point)
    
    if -EPSILON <= first_cross <= EPSILON:
        return True
    
    sign = 1 if first_cross > 0 else -1
    
    for i in range(1, n):
        cross = cross_product(poly[i], poly[(i + 1) % n], point)
        
        if -EPSILON <= cross <= EPSILON:
            return True
        
        if (cross > 0 and sign < 0) or (cross < 0 and sign > 0):
            return False
    
    return True
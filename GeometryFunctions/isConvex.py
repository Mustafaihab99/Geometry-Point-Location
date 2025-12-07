# zizo
import math
from GeometryFunctions.ensureCCW import ensure_ccw

def is_convex(polygon):
    """Check if a polygon is convex."""
    n = len(polygon)
    if n < 3:
        return False
    
    polygon = ensure_ccw(polygon)
    
    for i in range(n):
        A = polygon[i]
        B = polygon[(i + 1) % n]
        C = polygon[(i + 2) % n]
        
        cross = (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])
        if cross < 0:
            return False
    
    return True

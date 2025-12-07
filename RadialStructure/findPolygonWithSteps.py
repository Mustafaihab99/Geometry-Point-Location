# kiko
import math
from GeometryFunctions.pointInConvexPolygon import point_in_convex_polygon
from GeometryFunctions.ensureCCW import ensure_ccw
from GeometryFunctions.angle import angle

def find_polygon_with_steps(point, O, angles, sectors, subdivision, creating_polygon=None):
    """
    Find polygon containing the point and track binary search steps.
    Returns: (result_index, search_steps)
    """
    if creating_polygon and len(creating_polygon) >= 3:
        if point_in_convex_polygon(point, creating_polygon):
            return -2, []  
    
    for i, poly in enumerate(subdivision):
        if point_in_convex_polygon(point, poly):
            return i, []
    
    if not O or not angles or not sectors:
        return -1, []
    
    ang = angle(O, point)
    
    search_steps = []
    
    ang = ang % (2 * math.pi)
    
    if not angles:
        return -1, search_steps
    
    angles_extended = angles + [a + 2 * math.pi for a in angles]
    
    left = 0
    right = len(angles_extended) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        search_steps.append({
            'left': left % len(angles),
            'right': right % len(angles),
            'mid': mid % len(angles),
            'mid_value': angles_extended[mid],
            'target': ang,
            'condition': angles_extended[mid] <= ang
        })
        
        if angles_extended[mid] <= ang:
            left = mid + 1
        else:
            right = mid - 1
    
    position = right
    sector_index = position % len(angles)
    
    if sector_index >= len(sectors):
        return -1, search_steps
    
    face = sectors[sector_index]
    
    if face != -1 and face < len(subdivision):
        if point_in_convex_polygon(point, subdivision[face]):
            return face, search_steps
    
    return -1, search_steps
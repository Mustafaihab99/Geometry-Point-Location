import math


def point_to_line_distance(point, line_p1, line_p2):
    """Calculate distance from point to line segment."""
    x, y = point
    x1, y1 = line_p1
    x2, y2 = line_p2
    
    line_vec = (x2 - x1, y2 - y1)
    line_len_sq = line_vec[0]**2 + line_vec[1]**2
    
    if line_len_sq == 0:
        return distance(point, line_p1)
    
    t = max(0, min(1, ((x - x1) * line_vec[0] + (y - y1) * line_vec[1]) / line_len_sq))
    
    proj_x = x1 + t * line_vec[0]
    proj_y = y1 + t * line_vec[1]
    
    return distance(point, (proj_x, proj_y))
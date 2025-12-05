import math


def ensure_ccw(poly):
    """Ensure polygon vertices are in counter-clockwise order."""
    area = 0
    n = len(poly)
    for i in range(n):
        j = (i + 1) % n
        area += poly[i][0] * poly[j][1]
        area -= poly[j][0] * poly[i][1]
    
    if area < 0:
        return poly[::-1]
    return poly
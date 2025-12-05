import math

def binary_search_sector(ang, angles):
    """Binary search to find the appropriate sector."""
    if not angles:
        return 0
    
    ang = ang % (2 * math.pi)
    
    angles_extended = angles + [a + 2 * math.pi for a in angles]
    
    left = 0
    right = len(angles_extended) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if angles_extended[mid] <= ang:
            left = mid + 1
        else:
            right = mid - 1
    
    position = right
    sector_index = position % len(angles)
    
    return sector_index
# gorge
import math

def binary_search_sector(ang, angles):
    """Binary search to find the appropriate sector."""
    if not angles:
        return 0
    
    ang = ang % (2 * math.pi)
    n = len(angles)
    
    if ang >= angles[-1] or ang < angles[0]:
        return 0
    
    left = 0
    right = n - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if angles[mid] <= ang:
            next_mid = (mid + 1) % n
            if ang < angles[next_mid] or (next_mid == 0 and ang >= angles[-1]):
                return mid
            left = mid + 1
        else:
            right = mid - 1
    
    return 0
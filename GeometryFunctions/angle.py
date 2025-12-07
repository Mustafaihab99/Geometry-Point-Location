# zizo
import math

def angle(O, P):
    """Return angle of point P around center O."""
    return math.atan2(P[1] - O[1], P[0] - O[0])
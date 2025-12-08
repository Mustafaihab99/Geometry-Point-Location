# kiko
import math
from BinarySearchSector import binary_search_sector
from GeometryFunctions.pointInConvexPolygon import point_in_convex_polygon
from GeometryFunctions.ensureCCW import ensure_ccw
from GeometryFunctions.angle import angle

def find_polygon_with_steps(point, O, angles, sectors, subdivision, creating_polygon=None):
    """
    Find the polygon that contains the point using angular sectors.
    Returns (polygon_index, search_steps)
    """
    search_steps = []

    if creating_polygon and len(creating_polygon) >= 3:
        if point_in_convex_polygon(point, creating_polygon):
            return -2, search_steps

    for i, poly in enumerate(subdivision):
        if point_in_convex_polygon(point, poly):
            return i, search_steps

    if not O or not angles or not sectors:
        return -1, search_steps

    ang = angle(O, point)

    sector_index, bs_steps = binary_search_sector(ang, angles)
    search_steps.extend(bs_steps)

    if sector_index >= len(sectors):
        return -1, search_steps

    face = sectors[sector_index]

    if face != -1 and face < len(subdivision):
        if point_in_convex_polygon(point, subdivision[face]):
            return face, search_steps

    return -1, search_steps
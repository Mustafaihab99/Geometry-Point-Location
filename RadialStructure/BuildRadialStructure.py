import math 
from ComputeSmartCenterAndProbe import compute_smart_center_and_probe

from angle import angle
from ensureCCW import ensure_ccw
from pointInConvexPolygon import point_in_convex_polygon

def build_radial_structure(subdivision):
    subdivision = [ensure_ccw(poly) for poly in subdivision]
    
    O, probe_dist = compute_smart_center_and_probe(subdivision)

    angle_list = []
    for poly in subdivision:
        for v in poly:
            angle_list.append(angle(O, v))

    angle_list = sorted(set(angle_list))
    M = len(angle_list)
    sector_face = []

    for i in range(M):
        a1 = angle_list[i]
        a2 = angle_list[(i + 1) % M]
        if a2 <= a1:
            a2 += 2 * math.pi

        mid_angle = (a1 + a2) / 2
        direction = (math.cos(mid_angle), math.sin(mid_angle))

        test_point = (
            O[0] + direction[0] * probe_dist,
            O[1] + direction[1] * probe_dist
        )

        found = -1
        for idx, poly in enumerate(subdivision):
            if point_in_convex_polygon(test_point, poly):
                found = idx
                break

        sector_face.append(found)

    return O, angle_list, sector_face, subdivision

# mustafa
import math 
from ComputeSmartCenterAndProbe import compute_smart_center_and_probe

from angle import angle
from ensureCCW import ensure_ccw
from pointInConvexPolygon import point_in_convex_polygon


def build_radial_structure(subdivision):
    subdivision = [ensure_ccw(poly) for poly in subdivision]
    
    O, probe_dist = compute_smart_center_and_probe(subdivision)
    
    angle_data = []
    for poly_idx, poly in enumerate(subdivision):
        for vertex in poly:
            ang = angle(O, vertex)
            angle_data.append((ang, poly_idx))
    
    angle_data.sort(key=lambda x: x[0])
    
    unique_angles = []
    polygons_per_angle = []
    
    i = 0
    while i < len(angle_data):
        current_angle = angle_data[i][0]
        polygons = set()
        
        while i < len(angle_data) and math.isclose(angle_data[i][0], current_angle, rel_tol=1e-10):
            polygons.add(angle_data[i][1])
            i += 1
        
        unique_angles.append(current_angle)
        polygons_per_angle.append(list(polygons))
    
    M = len(unique_angles)
    sector_face = [-1] * M
    
    for i in range(M):
        a1 = unique_angles[i]
        a2 = unique_angles[(i + 1) % M]
        if a2 <= a1:
            a2 += 2 * math.pi
        
        mid_angle = (a1 + a2) / 2
        
        direction = (math.cos(mid_angle), math.sin(mid_angle))
        test_point = (
            O[0] + direction[0] * probe_dist,
            O[1] + direction[1] * probe_dist
        )
        
        found = -1
        for poly_idx in polygons_per_angle[i]:
            if point_in_convex_polygon(test_point, subdivision[poly_idx]):
                found = poly_idx
                break
        
        if found == -1:
            for poly_idx in range(len(subdivision)):
                if point_in_convex_polygon(test_point, subdivision[poly_idx]):
                    found = poly_idx
                    break
        
        sector_face[i] = found
    
    return O, unique_angles, sector_face, subdivision
import random
import math

def generate_convex_polygon(n_points=5, radius=10):
    angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n_points)])
    polygon = []
    for a in angles:
        r = radius * (0.6 + random.random() * 0.4)
        x = r * math.cos(a)
        y = r * math.sin(a)
        polygon.append((round(x, 2), round(y, 2)))
    return polygon


def generate_random_polygon(n_points=6, spread=10):
    pts = [(random.uniform(-spread, spread), random.uniform(-spread, spread))
           for _ in range(n_points)]
    cx = sum(p[0] for p in pts) / n_points
    cy = sum(p[1] for p in pts) / n_points
    pts = sorted(pts, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    return [(round(x, 2), round(y, 2)) for x, y in pts]


def generate_subdivision(rows=2, cols=2, cell_size=10):
    polys = []
    for r in range(rows):
        for c in range(cols):
            x1 = c * cell_size
            y1 = r * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            poly = [
                (x1, y1),
                (x2, y1),
                (x2, y2),
                (x1, y2)
            ]
            polys.append(poly)
    return polys


def edge_cases():
    return {
        "thin_polygon": [
            (0, 0), (10, 0.1), (10, 0), (0, 0.1)
        ],

        "collinear_points": [
            (0, 0), (5, 0), (10, 0), (10, 5), (0, 5)
        ],

        "almost_line": [
            (0, 0), (10, 0.01), (20, 0.02)
        ],

        "touching_polygons_shared_vertex": [
            [(0,0), (4,0), (4,4), (0,4)],
            [(4,4), (6,4), (6,6), (4,6)]
        ],

        "touching_polygons_shared_edge": [
            [(0,0),(4,0),(4,4),(0,4)],
            [(4,0),(8,0),(8,4),(4,4)]
        ],

        "very_large_polygon": [
            (0,0),(10000,0),(10000,10000),(0,10000)
        ]
    }


def build_dataset():
    dataset = {
        "convex_polygons": [generate_convex_polygon(random.randint(3, 8)) for _ in range(6)],
        "random_polygons": [generate_random_polygon(random.randint(4, 8)) for _ in range(6)],
        "subdivisions": [
            generate_subdivision(2, 2, 10),
            generate_subdivision(3, 2, 7)
        ],
        "edge_cases": edge_cases(),
    }
    return dataset


if __name__ == "_examples_":
    data = build_dataset()
    print("Convex Polygons:\n", data["convex_polygons"])
    print("\nRandom Polygons:\n", data["random_polygons"])
    print("\nSubdivisions:\n", data["subdivisions"])
    print("\nEdge Cases:\n", data["edge_cases"])
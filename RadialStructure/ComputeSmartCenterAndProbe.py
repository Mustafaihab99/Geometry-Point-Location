# omar 
import math 

def compute_smart_center_and_probe(subdivision):
    xs = []
    ys = []

    for poly in subdivision:
        for (x, y) in poly:
            xs.append(x)
            ys.append(y)

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    O = ((min_x + max_x) / 2, (min_y + max_y) / 2)

    width = max_x - min_x
    height = max_y - min_y
    diag = math.sqrt(width * width + height * height)

    probe = diag * 5

    return O, probe
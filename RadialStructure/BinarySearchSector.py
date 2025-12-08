# gorge
import math


def binary_search_sector(ang, angles):
    """Binary search to find the appropriate sector and record steps."""
    search_steps = []

    if not angles:
        return 0, search_steps

    ang = ang % (2 * math.pi)
    n = len(angles)

    # special case: before first or after last
    if ang >= angles[-1] or ang < angles[0]:
        search_steps.append({
            "left": None,
            "right": None,
            "mid": None,
            "target": ang,
            "condition": "special-case → return 0"
        })
        return 0, search_steps

    left = 0
    right = n - 1

    while left <= right:
        mid = (left + right) // 2

        # record current state
        search_steps.append({
            "left": left,
            "right": right,
            "mid": mid,
            "mid_value": angles[mid],
            "next_mid": (mid + 1) % n,
            "target": ang,
            "condition": "angles[mid] <= ang"
        })

        if angles[mid] <= ang:
            next_mid = (mid + 1) % n
            if ang < angles[next_mid] or (next_mid == 0 and ang >= angles[-1]):
                return mid, search_steps
            left = mid + 1
        else:
            right = mid - 1

    return 0, search_steps
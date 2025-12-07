# fadel
import math

def cross_product(O, A, B):
    """Calculate cross product of vectors OA and OB."""
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])

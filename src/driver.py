from FieldElement import FieldElement
from EllipticCurvePoint import EllipticCurvePoint

def main():
    """
    for p in [7, 11, 17, 31]:
        new_list = []
        for i in range(1, p-1, 1):
            a = FieldElement(p, i)
            new_list.append(a ** (p-1))
        print("p = ", p, "\n", new_list, "\n")
    """
    """
    points = [(2,4), (-1,-1), (18,77), (5,7)]
    for item in points:
        try:
            a = EllipticCurvePoint(5, 7, item[0], item[1])
            print(f"The point ({a.x}, {a.y}), is on the curve y^2 = x^3 + {a.a} * x + {a.b})")
        except ValueError as ve:
            print(f"The point ({item[0]}, {item[1]}), is not on the curve y^2 = x^3 + {5} * x + {7})")
    """
    """
    a = EllipticCurvePoint(5, 7, 2, 5)
    b = EllipticCurvePoint(5, 7, -1, -1)
    c = EllipticCurvePoint(5, 7, 3, -7)
    d = EllipticCurvePoint(5, 7, -1, -1)
    print(a + b)
    print(b + c)
    print(a + c)
    print(b + d)
    """
    prime = 223
    a = FieldElement(prime, 0)
    b = FieldElement(prime, 7)

    cartesian_points = [(170, 142), (60, 139), (47, 71), (17, 56), (143, 98), (76, 66)]
    finite_field_points = []
    for idx in range(0, len(cartesian_points), 2):
        p1 = EllipticCurvePoint(a, b, FieldElement(prime, cartesian_points[idx][0]), FieldElement(prime, cartesian_points[idx][1]))
        p2 = EllipticCurvePoint(a, b, FieldElement(prime, cartesian_points[idx+1][0]), FieldElement(prime, cartesian_points[idx+1][1]))
        new_point = p1 + p2
        finite_field_points.append(new_point)
        print(new_point)
    
    point_set = [(192, 105), (143, 98), (47, 71), (47, 71), (47, 71), (47, 71)]
    multiples = [2, 2, 2, 4, 8, 21]

    for idx in range(0, 6, 1):
        point = multiples[idx] * EllipticCurvePoint(a, b, point_set[idx][0], point_set[idx][1])
        print(point)

if __name__ == "__main__":
    main()

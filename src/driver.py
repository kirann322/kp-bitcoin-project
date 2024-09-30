from FieldElement import FieldElement
from EllipticCurvePoint import EllipticCurvePoint
from S256Field import S256Field, S256Point

def main():
    CONSTANT_GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    CONSTANT_GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    CONSTANT_G = S256Point(CONSTANT_GX, CONSTANT_GY)
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

    prime = 223
    points = [(192, 105), (17, 56), (200, 119), (1, 193), (42, 99)]
    for point in points:
        x, y = FieldElement(prime, point[0]), FieldElement(prime, point[1])
        y_2 = y * y
        x_3 = x * x * x
        on_curve = (y_2 == x_3 + FieldElement(prime, 7))
        print(f"{on_curve}, {point} is " + ("" if on_curve else "NOT ") + "on the elliptic curve y^2 = x^3 + 7")
    """
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
    """
    """
    prime = 223
    a = FieldElement(prime, 0)
    b = FieldElement(prime, 7)
    point_set = [(192, 105), (143, 98), (47, 71), (47, 71), (47, 71), (47, 71)]
    multiples = [2, 2, 2, 4, 8, 21]
    for idx in range(0, 6, 1):
        point = EllipticCurvePoint(a, b, FieldElement(prime, point_set[idx][0]), FieldElement(prime, point_set[idx][1]))
        for _ in range(0, multiples[idx]-1, 1):
            point += EllipticCurvePoint(a, b, FieldElement(prime, point_set[idx][0]), FieldElement(prime, point_set[idx][1]))
        print(point)
    
    print(3 * EllipticCurvePoint(a, b, FieldElement(prime, 47), FieldElement(prime, 71)) * 7)
    print(2 * EllipticCurvePoint(a, b, FieldElement(prime, 47), FieldElement(prime, 71)))
    print(5 * EllipticCurvePoint(a, b, FieldElement(prime, 47), FieldElement(prime, 71)))
    print(7 * EllipticCurvePoint(a, b, FieldElement(prime, 47), FieldElement(prime, 71)))
    print(2 * EllipticCurvePoint(a, b, FieldElement(prime, 47), FieldElement(prime, 71)) + 5 * EllipticCurvePoint(a, b, FieldElement(prime, 47), FieldElement(prime, 71)))
    """
    gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    p = 2**256 - 2**32 - 977
    print(gy**2 % p == (gx**3 + 7) % p)

    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    x = FieldElement(p, gx)
    y = FieldElement(p, gy)
    G = EllipticCurvePoint(FieldElement(p, 0), FieldElement(p, 7), x, y)
    print(n*CONSTANT_G)

if __name__ == "__main__":
    main()

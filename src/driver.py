from random import randint
from FieldElement import FieldElement
from EllipticCurvePoint import EllipticCurvePoint
from S256Field import S256Field, S256Point
from PrivateKey import PrivateKey

import hmac
import hashlib

def main():
    CONSTANT_N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
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
    """
    gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    p = 2**256 - 2**32 - 977
    print(gy**2 % p == (gx**3 + 7) % p)

    N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    x = FieldElement(p, gx)
    y = FieldElement(p, gy)
    G = EllipticCurvePoint(FieldElement(p, 0), FieldElement(p, 7), x, y)
    print(N*CONSTANT_G)
    
    N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    z = 0xbc62d4b80d9e36da29c16c5d4d9f11731f36052c72401a76c23c0fb5a9b74423
    r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
    s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
    px = 0x04519fac3d910ca7e7138f7013706f619fa8f033e6ec6e09370ea38cee6a7574
    py = 0x82b51eab8c27c66e26c858a079bcdf4f1ada34cec420cafc7eac1a42216fb6c4
    point = S256Point(px, py)
    s_inv = pow(s, N-2, N)
    u = z * s_inv % N
    v = r * s_inv % N
    print((u*CONSTANT_G + v*point).x.num == r)

    px = 0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c
    py = 0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34
    point = S256Point(px, py)

    z = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60
    r = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
    s = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
    u = z * pow(s, N-2, N) % N
    v = r * pow(s, N-2, N) % N
    print((u*CONSTANT_G + v*point).x.num == r)

    z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
    r = 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c
    s = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6
    u = z * pow(s, N-2, N) % N
    v = r * pow(s, N-2, N) % N
    print((u*CONSTANT_G + v*point).x.num == r)
    """
    """
    e = 12345
    z = int.from_bytes(hashlib.sha256(hashlib.sha256(b'Programming Bitcoin!').digest()).digest(), 'big')
    k = 1234567890
    r = (k*CONSTANT_G).x.num
    k_inv = pow(k, CONSTANT_N-2, CONSTANT_N)
    s = (z+r*e) * k_inv % CONSTANT_N
    print(e*CONSTANT_G)
    print(hex(z))
    print(hex(r))
    print(hex(s))
    """
    priv = PrivateKey(5000)
    print(priv.point.sec(compressed=False).hex())
    priv = PrivateKey(2018**5)
    print(priv.point.sec(compressed=False).hex())
    priv = PrivateKey(0xdeadbeef12345)
    print(priv.point.sec(compressed=False).hex())

if __name__ == "__main__":
    main()

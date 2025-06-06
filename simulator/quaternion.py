import numpy as np

class Quaternion:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.norm = np.sqrt(self.a ** 2 + self.b ** 2 + self.c ** 2 + self.d ** 2)

    def __mul__(self, other):
        a = self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d
        b = self.a * other.b + self.b * other.a + self.c * other.d - self.d * other.c
        c = self.a * other.c - self.b * other.d + self.c * other.a + self.d * other.b
        d = self.a * other.d + self.b * other.c - self.c * other.b + self.d * other.a
        return Quaternion(a, b, c, d)

    def normalize(self):
        self.a /= self.norm
        self.b /= self.norm
        self.c /= self.norm
        self.d /= self.norm

    def denormalize(self, x):
        self.a *= x
        self.b *= x
        self.c *= x
        self.d *= x

    def conjugate(self):
        return Quaternion(self.a, -self.b, -self.c, -self.d)

    @staticmethod
    def from_angles(x, y, z):
        x_q = Quaternion(np.cos(np.pi * x / 360), np.sin(np.pi * x / 360), 0, 0)
        y_q = Quaternion(np.cos(np.pi * y / 360), 0, np.sin(np.pi * y / 360), 0)
        z_q = Quaternion(np.cos(np.pi * z / 360), 0, 0, np.sin(np.pi * z / 360))
        x_q.normalize()
        y_q.normalize()
        z_q.normalize()
        rotated_vector = z_q * y_q * x_q
        return rotated_vector

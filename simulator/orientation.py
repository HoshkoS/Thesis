import numpy as np
from .quaternion import Quaternion

def rotate_vector(vector, rotation):
    rotation.normalize()
    quaternion_vector = Quaternion(0, vector[0], vector[1], vector[2])
    rotated_vector = rotation * quaternion_vector * rotation.conjugate()
    return np.array([rotated_vector.b, rotated_vector.c, rotated_vector.d])

def turn_plane(points, q):
    return np.array([rotate_vector(i, q) for i in points])

def get_rotation_matrix(roll, pitch, yaw, degrees=True):
    if degrees:
        roll = np.radians(roll)
        pitch = np.radians(pitch)
        yaw = np.radians(yaw)

    rx = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])

    ry = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])

    rz = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])

    R = rz @ ry @ rx
    return R

def rotate_point_by_matrix(point, rotation_matrix):
    rotated_point = rotation_matrix @ point
    return rotated_point

def turn_plane_by_rotmat(points, rotation_matrix):
    return np.array([rotate_point_by_matrix(i, rotation_matrix) for i in points])

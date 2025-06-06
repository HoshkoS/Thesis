
import pyvista as pv
import numpy as np
import time
from scipy.spatial.transform import Rotation as R
from .quaternion import Quaternion
from .orientation import turn_plane, rotate_vector, get_rotation_matrix, rotate_point_by_matrix, turn_plane_by_rotmat

def run(angle_x, angle_y, angle_z, speed, use_quaternion, use_euler, use_matrix, steps):
    delta_time = 0.2
    angle_x = speed * delta_time * angle_x
    angle_y = speed * delta_time * angle_y
    angle_z = speed * delta_time * angle_z

    planes = []
    plane = pv.read("./objects/airplane.obj")
    plane = plane.rotate_x(90)
    floor = pv.Plane(center=(0, 0, -50), direction=(0, 0, 1), i_size=800, j_size=800)
    plotter = pv.Plotter(off_screen=True, window_size=[800, 600])
    plane = plane.translate([0, -100, 0])
    if angle_z < 0:
        plane = plane.translate([-100,0,0])
    elif angle_z > 0:
        plane = plane.translate([100, 0, 0])
    if angle_x != 0 or angle_y != 0:
        floor = floor.translate([0, 0, -150])

    plane2 = 0
    plane3 = 0

    if use_euler:
        plane2 = plane.copy()
        planes.append(("purple", plane2))

    if use_matrix:
        plane3 = plane.copy()
        planes.append(("green", plane3))

    if use_quaternion:
        planes.append(("blue", plane))

    for color, obj in planes:
        plotter.add_mesh(obj, color=color)


    plotter.add_mesh(floor, color='lightgray')
    plotter.add_axes()
    plotter.camera_position = "iso"

    plotter.camera.zoom(1.4)

    plotter.open_gif("./simulations/airplane_quaternion.gif")

    quat = Quaternion.from_angles(angle_x, angle_y, angle_z)
    rotation_euler = R.from_euler('xyz', [angle_x,angle_y, angle_z], degrees=True)
    rotation_matrix = get_rotation_matrix(angle_x, angle_y, angle_z)

    direction1 = np.array([0, 1, 0])
    direction2 = np.array([0, 1, 0])
    direction3 = np.array([0, 1, 0])

    for i in range(steps):
        if i == steps - 1:
            if use_quaternion:
                start = time.time()
                plane.points = turn_plane(plane.points, quat)
                plane.points += rotate_vector(direction1, quat) * speed * delta_time
                t_q = time.time() - start
                print(t_q)
            if use_euler:
                start = time.time()
                plane2.points = rotation_euler.apply(plane2.points)
                plane2.points += rotation_euler.apply(direction2) * speed * delta_time
                t_q = time.time() - start
                print(t_q)
            if use_matrix:
                start = time.time()
                plane3.points = turn_plane_by_rotmat(plane3.points, rotation_matrix)
                plane3.points += rotate_point_by_matrix(direction3, rotation_matrix) * speed * delta_time
                t_q = time.time() - start
                print(np.average(plane.points - plane3.points))
                print(t_q)
            continue
        if use_quaternion:
            plane.points = turn_plane(plane.points, quat)
            plane.points += rotate_vector(direction1, quat) * speed * delta_time
        if use_euler:
            plane2.points = rotation_euler.apply(plane2.points)
            plane2.points += rotation_euler.apply(direction2) * speed * delta_time
        if use_matrix:
            plane3.points = turn_plane_by_rotmat(plane3.points, rotation_matrix)
            plane3.points += rotate_point_by_matrix(direction3, rotation_matrix) * speed * delta_time

        plotter.write_frame()

    plotter.close()

    print("GIF створено.")

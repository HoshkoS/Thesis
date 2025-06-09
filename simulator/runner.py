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

    base_plane = pv.read("./objects/airplane.obj").rotate_x(90).translate([0, -100, 0])
    floor = pv.Plane(center=(0, 0, -50), direction=(0, 0, 1), i_size=800, j_size=800)
    if angle_z < 0:
        base_plane = base_plane.translate([-100, 0, 0])
    elif angle_z > 0:
        base_plane = base_plane.translate([100, 0, 0])
    if angle_x != 0 or angle_y != 0:
        floor = floor.translate([0, 0, -150])

    plane_q = base_plane.copy() if use_quaternion else None
    plane_e = base_plane.copy() if use_euler else None
    plane_m = base_plane.copy() if use_matrix else None

    quat = Quaternion.from_angles(angle_x, angle_y, angle_z)
    rotation_euler = R.from_euler('xyz', [angle_x, angle_y, angle_z], degrees=True)
    rotation_matrix = get_rotation_matrix(angle_x, angle_y, angle_z)

    direction = np.array([0, 1, 0])
    plotter_xy = 0
    plotter_yz = 0
    plotter_xz = 0

    views = [
        ("xy", [(0, 0, 1000), (0, 0, 0), (0, 1, 0)]),
        ("yz", [(1000, 0, 0), (0, 0, 0), (0, 0, 1)]),
        ("xz", [(0, 1000, 0), (0, 0, 0), (0, 0, 1)]),
    ]

    plotter = pv.Plotter(off_screen=True, window_size=[800, 600])
    if views:
        plotter_xy = pv.Plotter(off_screen=True, window_size=[800, 600])
        plotter_yz = pv.Plotter(off_screen=True, window_size=[800, 600])
        plotter_xz = pv.Plotter(off_screen=True, window_size=[800, 600])
        for i in [plotter_xy, plotter_yz, plotter_xz]:
            i.add_mesh(floor, color='lightgray')
            if use_quaternion:
                i.add_mesh(plane_q, color='blue')
            if use_euler:
                i.add_mesh(plane_e, color='purple')
            if use_matrix:
                i.add_mesh(plane_m, color='green')
            i.add_axes()
        plotter_xy.camera_position = [(0, 0, 1000), (0, 0, 0), (0, 1, 0)]
        plotter_yz.camera_position =  [(1000, 0, 0), (0, 0, 0), (0, 0, 1)]
        plotter_xz.camera_position = [(0, 1000, 0), (0, 0, 0), (0, 0, 1)]

    plotter.add_mesh(floor, color='lightgray')
    if use_quaternion:
        plotter.add_mesh(plane_q, color='blue')
    if use_euler:
        plotter.add_mesh(plane_e, color='purple')
    if use_matrix:
        plotter.add_mesh(plane_m, color='green')
    plotter.add_axes()
    plotter.camera_position = "iso"

    plotter.camera.zoom(1.4)

    plotter.open_gif("./simulations/airplane_quaternion.gif")
    if views:
        plotter_xy.open_gif("./simulations/airplane_view_xy.gif")
        plotter_yz.open_gif("./simulations/airplane_view_yz.gif")
        plotter_xz.open_gif("./simulations/airplane_view_xz.gif")

    dir_q = direction.copy()
    dir_e = direction.copy()
    dir_m = direction.copy()

    for i in range(steps):
        if i == steps - 1:
            if use_quaternion:
                start = time.time()
                plane_q.points = turn_plane(plane_q.points, quat)
                plane_q.points += rotate_vector(dir_q, quat) * speed * delta_time
                t_q = time.time() - start
                print(t_q)
            if use_euler:
                start = time.time()
                plane_e.points = rotation_euler.apply(plane_e.points)
                plane_e.points += rotation_euler.apply(dir_e) * speed * delta_time
                t_q = time.time() - start
                print(t_q)
            if use_matrix:
                start = time.time()
                plane_m.points = turn_plane_by_rotmat(plane_m.points, rotation_matrix)
                plane_m.points += rotate_point_by_matrix(dir_m, rotation_matrix) * speed * delta_time
                t_q = time.time() - start
                print(np.average(plane_q.points - plane_m.points))
                print(t_q)
            continue
        if use_quaternion:
            plane_q.points = turn_plane(plane_q.points, quat)
            plane_q.points += rotate_vector(dir_q, quat) * speed * delta_time

        if use_euler:
            plane_e.points = rotation_euler.apply(plane_e.points)
            plane_e.points += rotation_euler.apply(dir_e) * speed * delta_time

        if use_matrix:
            plane_m.points = turn_plane_by_rotmat(plane_m.points, rotation_matrix)
            plane_m.points += rotate_point_by_matrix(dir_m, rotation_matrix) * speed * delta_time

        plotter.write_frame()
        if views:
            plotter_xy.write_frame()
            plotter_yz.write_frame()
            plotter_xz.write_frame()


    plotter.close()
    if views:
        plotter_xy.close()
        plotter_yz.close()
        plotter_xz.close()
    print("GIF створено.")

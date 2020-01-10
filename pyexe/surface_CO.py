#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random


def sph2cart(phi, theta, r):
    x = list(map(lambda a, b, c:a*b*c, np.sin(theta), np.cos(phi), r))
    y = list(map(lambda a, b, c:a*b*c, np.sin(theta), np.sin(phi), r))
    z = list(map(lambda a, b:a*b, np.cos(theta), r))
    return x, y, z

if __name__ == '__main__':
    plt.close()
    n_vector = 100
    len_vector = 0.5
    # sphere
    theta_sph, phi_sph = np.linspace(-0.5 * np.pi, 0.5 * np.pi, 30), np.linspace(0, 2 * np.pi, 30)
    r_sph = 1
    x_sph = r_sph * np.outer(np.cos(phi_sph), np.sin(theta_sph))
    y_sph = r_sph * np.outer(np.sin(phi_sph), np.sin(theta_sph))
    z_sph = r_sph * np.outer(np.ones(np.size(phi_sph)), np.cos(theta_sph))

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    plot = ax1.plot_surface(x_sph, y_sph, z_sph, rstride=1, cstride=1,
                        antialiased=False, alpha=0.5, linewidth=0, color='orange')
    ax1.set_title('Sphere')
    ax1.set_xlim([-(r_sph+len_vector), r_sph+len_vector])
    ax1.set_ylim([-(r_sph+len_vector), r_sph+len_vector])
    ax1.set_zlim([-(r_sph+len_vector), r_sph+len_vector])
    ax1.set_aspect("equal")
    plt.xlabel('x')
    plt.ylabel('y')
    # vectors on sphere
    phi_0_sph = 2 * np.pi * np.random.rand(n_vector)
    theta_0_sph = np.pi * (np.random.rand(n_vector) - 0.5)
    r_0_sph = r_sph * np.ones(n_vector)
    x_0_sph, y_0_sph, z_0_sph = sph2cart(phi_0_sph, theta_0_sph, r_0_sph)
    u_sph, v_sph, w_sph = sph2cart(phi_0_sph, theta_0_sph, len_vector * np.ones(n_vector))
    ax1.quiver(x_0_sph, y_0_sph, z_0_sph, u_sph, v_sph, w_sph)

    # plane
    r_max_plane = np.sqrt(2) * r_sph # maintain same surface area
    r_plane, phi_plane = np.linspace(0, r_max_plane, 30), np.linspace(0, 2 * np.pi, 30)
    theta_plane = 0.5 * np.pi
    x_plane = np.sin(theta_plane) * np.outer(np.cos(phi_plane), r_plane)
    y_plane = np.sin(theta_plane) * np.outer(np.sin(phi_plane), r_plane)
    z_plane = np.cos(theta_plane) * np.outer(np.ones(np.size(phi_plane)), r_plane)

    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    plot = ax2.plot_surface(x_plane, y_plane, z_plane, rstride=1, cstride=1,
                            antialiased=False, alpha=0.5, linewidth=0, color='orange')
    ax2.set_title('Plane')
    ax2.set_xlim([-r_max_plane, r_max_plane])
    ax2.set_ylim([-r_max_plane, r_max_plane])
    ax2.set_zlim([-len_vector, len_vector])
    ax2.set_aspect("equal")

    # vectors on plane
    phi_0_plane = 2 * np.pi * np.random.rand(n_vector)
    theta_0_plane = 0.5 * np.pi * np.ones(n_vector)
    r_0_plane = r_max_plane * np.random.rand(n_vector)
    x_0_plane, y_0_plane, z_0_plane = sph2cart(phi_0_plane, theta_0_plane, r_0_plane)
    u_plane = v_plane = np.zeros(n_vector)
    w_plane = len_vector * np.ones(n_vector)

    ax2.quiver(x_0_plane, y_0_plane, z_0_plane, u_plane, v_plane, w_plane)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
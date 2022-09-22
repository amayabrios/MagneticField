import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


class Bfield:
    def __init__(self, B0: float, RE: float, rad: float):
        # Mean magnitude of the Earth's magnetic field at the equator in T
        self.B0 = B0
        # Radius of Earth, Mm (10^6 m: mega-metres!)
        self.RE = RE
        # Deviation of magnetic pole from axis
        self.alpha = np.radians(rad)

    nx, ny = 64, 64
    XMAX, YMAX = 40, 40
    x = np.linspace(-XMAX, XMAX, nx)
    y = np.linspace(-YMAX, YMAX, ny)

    def B(self, r, theta):
        # Return the magnetic field vector at (r, theta)
        fac = self.B0 * (self.RE / r)**3
        return -2 * fac * np.cos(theta + self.alpha), -fac * np.sin(theta + self.alpha)

    def Bcomponents(self):
        # Grid of x, y points on a Cartesian grid
        X, Y = np.meshgrid(self.x, self.y)
        r, theta = np.hypot(X, Y), np.arctan2(Y, X)

        # Magnetic field vector, B = (Ex, Ey), as separate components
        Br, Btheta = self.B(r, theta)
        # Transform to Cartesian coordinates: NB make North point up, not to the right.
        c, s = np.cos(np.pi/2 + theta), np.sin(np.pi/2 + theta)
        Bx = -Btheta * s + Br * c
        By = Btheta * c + Br * s
        return Bx, By

    def display(self):
        fig, ax = plt.subplots()
        Bx, By = self.Bcomponents()

        # Plot the streamlines with an appropriate colormap and arrow style
        color = 2 * np.log(np.hypot(Bx, By))
        ax.streamplot(self.x, self.y, Bx, By, color=color, linewidth=1, cmap=plt.cm.inferno, density=2,
                      arrowstyle='->', arrowsize=1.5)

        # Add marker for  Earth
        ax.add_patch(Circle((0, 0), self.RE, color='b', zorder=50))

        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        ax.set_xlim(-self.XMAX, self.XMAX)
        ax.set_ylim(-self.YMAX, self.YMAX)
        ax.set_aspect('equal')
        plt.show()


mag_field = Bfield(3.12e-5, 6.370, 9.6)
mag_field.display()

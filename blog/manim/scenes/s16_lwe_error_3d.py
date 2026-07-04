from manim import *
import numpy as np

class LWEError3D(ThreeDScene):
    def construct(self):
        # Set up camera for an isometric 3D view
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Draw 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 2, 0.5],
            x_length=8,
            y_length=8,
            z_length=4
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label("e_1")
        y_label = axes.get_y_axis_label("e_2")
        
        # Create a 3D discrete Gaussian surface
        def gaussian_surface(u, v):
            x = u
            y = v
            # standard normal distribution, scaled
            z = np.exp(-(x**2 + y**2) / 2) * 1.5
            return np.array([x, y, z])
            
        surface = Surface(
            lambda u, v: axes.c2p(*gaussian_surface(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            checkerboard_colors=[BLUE_D, BLUE_E],
            resolution=(30, 30),
            fill_opacity=0.5
        )
        
        # Animate the creation of the mathematical environment
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=2)
        self.play(Create(surface), run_time=2)
        
        # Rotate the camera slowly while sampling points
        self.begin_ambient_camera_rotation(rate=0.1)
        
        # Sample points and snap them to the discrete integer lattice
        for _ in range(8):
            # Sample from normal distribution
            x = np.random.normal(0, 0.8)
            y = np.random.normal(0, 0.8)
            z = np.exp(-(x**2 + y**2) / 2) * 1.5
            
            # The continuous sample point
            sample_dot = Sphere(radius=0.1).set_color(YELLOW).move_to(axes.c2p(x, y, z))
            
            # The nearest integer on the 2D grid
            grid_x, grid_y = round(x), round(y)
            grid_dot = Sphere(radius=0.1).set_color(RED).move_to(axes.c2p(grid_x, grid_y, 0))
            
            # Draw a line snapping the continuous value to the discrete grid
            snap_line = DashedLine(
                axes.c2p(x, y, z),
                axes.c2p(grid_x, grid_y, 0),
                color=RED
            )
            
            self.play(FadeIn(sample_dot), run_time=0.4)
            self.play(Create(snap_line), run_time=0.4)
            self.play(ReplacementTransform(sample_dot, grid_dot), FadeOut(snap_line), run_time=0.6)
            self.play(FadeOut(grid_dot), run_time=0.4)
            
        self.stop_ambient_camera_rotation()
        self.wait(1)

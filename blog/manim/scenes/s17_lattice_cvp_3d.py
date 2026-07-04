from manim import *
import numpy as np

class LatticeCVP3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        axes = ThreeDAxes()
        self.play(Create(axes))
        
        # Define 3 basis vectors for the lattice
        b1 = np.array([2, 0.5, 0.2])
        b2 = np.array([0.5, 2, 0.5])
        b3 = np.array([0.2, 0.5, 2])
        
        # Generate lattice points
        points = VGroup()
        for i in range(-2, 3):
            for j in range(-2, 3):
                for k in range(-2, 3):
                    pos = i*b1 + j*b2 + k*b3
                    # Only add points near origin to avoid clutter
                    if np.linalg.norm(pos) < 5:
                        points.add(Sphere(radius=0.08).set_color(BLUE).move_to(axes.c2p(*pos)))
                        
        self.play(FadeIn(points, lag_ratio=0.05), run_time=3)
        self.begin_ambient_camera_rotation(rate=0.2)
        
        # The true secret point on the grid
        secret_pos = 1*b1 + 1*b2 + 1*b3
        
        # The LWE sample with error (suspended near the secret point)
        error = np.array([0.4, -0.3, 0.5])
        lwe_sample = secret_pos + error
        
        sample_dot = Sphere(radius=0.15).set_color(RED).move_to(axes.c2p(*lwe_sample))
        self.play(FadeIn(sample_dot))
        
        # Draw a search sphere to show Closest Vector Problem search space
        search_sphere = Surface(
            lambda u, v: axes.c2p(*(lwe_sample + 0.8 * np.array([
                np.cos(u)*np.sin(v),
                np.sin(u)*np.sin(v),
                np.cos(v)
            ]))),
            u_range=[0, 2*PI],
            v_range=[0, PI],
            checkerboard_colors=[RED_E, RED_D],
            fill_opacity=0.3,
            resolution=(15, 15)
        )
        self.play(Create(search_sphere), run_time=2)
        self.wait(1)
        
        # Snap to closest grid point
        snap_line = DashedLine(axes.c2p(*lwe_sample), axes.c2p(*secret_pos), color=YELLOW)
        self.play(Create(snap_line))
        self.play(sample_dot.animate.move_to(axes.c2p(*secret_pos)), run_time=1)
        
        self.stop_ambient_camera_rotation()
        self.wait(1)

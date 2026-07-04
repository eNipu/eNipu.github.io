from manim import *
import numpy as np

class NoiseSphereBoundary(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        self.play(Create(axes))
        
        # Draw the spherical noise budget boundary (radius = 2.5)
        # Anything inside this sphere decrypts successfully.
        budget_radius = 2.5
        sphere = Surface(
            lambda u, v: axes.c2p(*(budget_radius * np.array([
                np.cos(u)*np.sin(v),
                np.sin(u)*np.sin(v),
                np.cos(v)
            ]))),
            u_range=[0, 2*PI],
            v_range=[0, PI],
            color=BLUE_E,
            fill_opacity=0.15,
            resolution=(24, 24)
        )
        self.play(Create(sphere))
        
        self.begin_ambient_camera_rotation(rate=0.2)
        
        # Start with a small noise vector at the origin representing a fresh encryption
        noise_vec = np.array([0.2, 0.3, -0.1])
        arrow = Arrow3D(
            start=axes.c2p(*ORIGIN), 
            end=axes.c2p(*noise_vec), 
            color=GREEN
        )
        self.play(Create(arrow))
        
        # Animate homomorphic operations (adding ciphertexts) causing the noise vector to grow
        for i in range(6):
            # Homomorphic addition adds a small random chunk to the noise
            step = np.random.normal(0, 0.6, 3)
            noise_vec = noise_vec + step
            
            # Check if the noise vector has pierced the outer sphere boundary
            current_radius = np.linalg.norm(noise_vec)
            
            # It turns red and decryption fails if it crosses the boundary
            color = GREEN if current_radius <= budget_radius else RED
                
            new_arrow = Arrow3D(
                start=axes.c2p(*ORIGIN), 
                end=axes.c2p(*noise_vec), 
                color=color
            )
            
            # Animate the vector growing/shifting
            self.play(Transform(arrow, new_arrow), run_time=0.8)
            self.wait(0.2)
            
            if color == RED:
                # Stop simulating once the budget is exhausted
                # Add a brief text indicator
                fail_text = Text("Decryption Failure!", color=RED).to_corner(UL)
                # Keep text static while scene rotates by using fixed in frame
                self.add_fixed_in_frame_mobjects(fail_text)
                self.play(Write(fail_text))
                break
                
        self.stop_ambient_camera_rotation()
        self.wait(2)

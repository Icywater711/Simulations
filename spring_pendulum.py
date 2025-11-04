import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

g = 9.81 #m/s^2
k = 30.0 #N/m
L0 = 8.0 #m
m = 1.0 #kg
dt = 0.01
steps = 3000


r = np.array([5.0, np.pi/2]) #positions, length of spring and angle to the vertical respectively 
v = np.array([0.0, -1.0]) #velocities, radial and angular respectively
a = np.array([0.0, 0.0]) #accelerations, radial and angular respectively
trajectories =[]
for _ in range(steps):
    
    # equations of motion from the Euler-Lagrange equations
    a[0] = r[0]*v[1]**2 - (k/m)*(r[0]-L0) + g*np.cos(r[1])
    a[1] = (-2*v[0]*v[1] - g*np.sin(r[1]))/r[0]
    v += a*dt
    r += v*dt
    R = [ 
        np.array([r[0]*np.sin(r[1]), 5-r[0]*np.cos(r[1])])
    ]
    trajectories.append(R.copy())
trajectories = np.array(trajectories)

#animation setup
fig, ax = plt.subplots(figsize=(8,8), dpi = 300)
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor("black")
fig.patch.set_facecolor("black")

dot, = ax.plot([], [], 'o', color = 'blue', markersize=6)
line, = ax.plot([], [], '-', color = 'red', lw=1.0)
line2, = ax.plot( [0,0], [0,0], '-', color = 'white', lw=1.0)

def update(frame):
    line.set_data( [0, trajectories[frame,0,0]], [5, trajectories[frame,0,1]])
    dot.set_data( [trajectories[frame,0,0]], [trajectories[frame,0,1]])
    line2.set_data( trajectories[:frame,0,0], trajectories[:frame,0,1])
    return line, dot, line2


def init():
    line.set_data([], [])
    dot.set_data([], [])
    line2.set_data([], [])
    return line, dot, line2
    

ani = animation.FuncAnimation(fig, update, frames=steps, init_func=init, blit=True, interval=10)

ani.save("Spring Pendulum.mp4", fps=120, extra_args=['-vcodec', 'libx264'])



    
    

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

g = 9.81 #m/s^2
m1 = 1.0 #kg
m2 = 1.0 #kg
dt = 0.01
steps = 9000
L1 = 5.0 #m
L2 = 10.0 #m

o = [np.pi/2, np.pi/2] #angles
w = [-1.5,-1.0] #angular velocities
a = [0.0, 0.0] #angular accelerations
r = [0.0, 0.0] #positions
o = np.array(o)
w = np.array(w)
a = np.array(a)
trajectories =[]
for _ in range(steps):
    
    # equations of motion from the Euler-Lagrange equations
    a[0] = (-g*(2*m1 + m2)*np.sin(o[0]) - m2*g*np.sin(o[0] - 2*o[1]) - 2*np.sin(o[0] - o[1])*m2*(w[1]**2*L2 + w[0]**2*L1*np.cos(o[0] - o[1]))) / (L1 * (2*m1 + m2 - m2*np.cos(2*o[0] - 2*o[1])))
    a[1] = (2*np.sin(o[0] - o[1]) * (w[0]**2*L1*(m1 + m2) + g*(m1 + m2)*np.cos(o[0]) + w[1]**2*L2*m2*np.cos(o[0] - o[1]))) / (L2 * (2*m1 + m2 - m2*np.cos(2*o[0] - 2*o[1])))
    w += a*dt
    o += w*dt
    r = [ 
        np.array([L1*np.sin(o[0]), 5-L1*np.cos(o[0])]),
        np.array([L1*np.sin(o[0])+L2*np.sin(o[1]), 5-L1*np.cos(o[0])-L2*np.cos(o[1])])
    ]
    trajectories.append(r.copy())
trajectories = np.array(trajectories)

#animation setup
fig, ax = plt.subplots(figsize=(10,10), dpi=300)
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_aspect('equal')
ax.axis('off')



line2, = ax.plot([], [], 'o-', color = 'red', markersize=0.5, lw=0.5)
line3, = ax.plot([], [], '-', color = 'black', lw=1.0)
line4, = ax.plot([], [], '-', color = 'black', lw=1.0) 
dot1, = ax.plot([], [], 'o', color = 'blue', markersize=12)
dot2, = ax.plot([], [], 'o', color = 'red', markersize=12)

def update(frame):
    line2.set_data([trajectories[:frame, 1,0], trajectories[:frame, 1,1]])
    line3.set_data([[0,trajectories[frame, 0,0]], [5, trajectories[frame, 0,1]]])
    line4.set_data([trajectories[frame, 0,0], trajectories[frame, 1,0]], [trajectories[frame,0,1], trajectories[frame,1,1]])
    dot1.set_data([trajectories[frame, 0,0]], [trajectories[frame, 0,1]])
    dot2.set_data([trajectories[frame, 1,0]], [trajectories[frame, 1,1]])
    return line2, line3, line4, dot1, dot2

def init():
    line2.set_data([], [])
    line3.set_data([], [])
    line4.set_data([], [])
    dot1.set_data([], [])
    dot2.set_data([], [])
    return line2, line3, line4, dot1, dot2

ani = animation.FuncAnimation(fig, update, frames=steps, init_func=init, blit=True, interval=10)

ani.save("Double_Pendulum.mp4", fps=120, extra_args=['-vcodec', 'libx264'])



    
    

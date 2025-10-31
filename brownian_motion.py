import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

dt = 0.01  # time step
steps = 1000  # number of time steps
speed = 10  # speed of particles
nx, ny = 10, 10 # create a grid with a particle at each point
x = np.linspace(-10, 10, nx)
y = np.linspace(-10, 10, ny)
X, Y = np.meshgrid(x, y)
r = []
v=[]
for i in range(nx):
    for j in range(ny):
        r.append([X[i,j], Y[i,j]]) # intial positions
        
        # randomize velocity components
        x = np.random.uniform(0,10) 
        y = np.random.uniform(0,10)  
        v.append([x,y]/np.sqrt(x**2+y**2))  # Try to replace later with a bell curve distribution
r = np.array(r)
v = speed*np.array(v)
trajectories = [r.copy()]

for _ in range(steps):
    # conservation of momentum at collisions with each other
    for i in range(len(r)):
        for j in range(len(r)):
            if i != j:
                d = np.linalg.norm(r[i]-r[j])
                if d <= 0.75:  # assuming each particle has a radius of 0.25
                    v_i_initial = v[i].copy()
                    v_j_initial = v[j].copy()
                    v[i] = v_i_initial - np.dot(v_i_initial - v_j_initial, r[i] - r[j]) / d**2 * (r[i] - r[j])
                    v[j] = v_j_initial - np.dot(v_j_initial - v_i_initial, r[j] - r[i]) / d**2 * (r[j] - r[i])
    for i in range(len(r)):
        if r[i,0] <= -10 or r[i,0] >= 10:  # collision with vertical walls
            v[i,0] = -v[i,0]
        if r[i,1] <= -10 or r[i,1] >= 10:  # collision with horizontal walls
            v[i,1] = -v[i,1]
    # update positions
    r += v*dt
    trajectories.append(r.copy())
trajectories = np.array(trajectories)

#animation setup
fig, ax = plt.subplots()
ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
ax.set_aspect('equal')

dots = []
for i in range(len(r)-1):
    dot, = ax.plot([], [], 'o', color = 'blue', markersize=5)
    dots.append(dot)
dots.append(ax.plot([], [], 'o', color = 'red', markersize=5)[0])  # last particle in red
line, = ax.plot([], [], '-', color = 'black', lw=1.0)

def update(frame):
    for i in range(len(r)):
        dots[i].set_data([trajectories[frame, i, 0]], [trajectories[frame, i, 1]])
    line.set_data(trajectories[:frame, len(r)-1, 0], trajectories[:frame, len(r)-1, 1])
    return tuple(dots)

def init():
    for i in range(len(r)):
        dots[i].set_data([],[])
    line.set_data([], [])
    return tuple(dots)

ani = animation.FuncAnimation(fig, update, frames=len(trajectories), init_func=init, blit=True, interval=10)

ani.save("Brownian_motion.mp4", fps=30, extra_args=['-vcodec', 'libx264'])

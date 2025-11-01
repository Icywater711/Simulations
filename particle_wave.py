import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

# constants
N = 20  # number of spheres
v = 5.0  # speed of sphere
L = 40.0  # length of the box
particles = []
dt = 0.01  # time step
steps = 1000  # number of time steps

# initial positions and directions
for i in range(N):
    particles.append([i*L/N,0])

particles[0][1] = v
particles = np.array(particles)
trajectories= [particles.copy()]

for _ in range(steps):
    for i in range(N):
        if i < N-1:
            if particles[i][0] > particles[i+1][0]-1 and particles[i][1] > 0:
                particles[i][1] = 0
                particles[i+1][1]= v
            if particles[i][0] < particles[i-1][0]+1 and particles[i][1] < 0:
                particles[i][1] = 0
                particles[i-1][1]= -v
        elif i== N-1:
            break
        if particles[i][0] >= 40:
            particles[i][1] = -v # reverse direction on hitting right wall
        if particles[i][0] <= 0:
            particles[i][1] = v  # reverse direction on hitting left wall
    particles[:,0] += particles[:, 1]*dt
    trajectories.append(particles.copy())

trajectories = np.array(trajectories)



#animation setup
fig, ax = plt.subplots(figsize=(10,10), dpi=100)
ax.set_xlim(0,50)
ax.set_ylim(-20,20)
ax.set_aspect('equal')
ax.axis('off')

dots = []
for i in range(N):
    if i % 2==0:
        dot, = ax.plot([], [], 'o', color = 'red', markersize=10)
    elif i % 3 == 0:
        dot, = ax.plot([], [], 'o', color = 'blue', markersize=10)
    else:
        dot, = ax.plot([], [], 'o', color = 'green', markersize=10)
    dots.append(dot)

def update(frame):
    for i in range(N):
        dots[i].set_data([trajectories[frame, i, 0]], [0])
    return tuple(dots)
    
def init():
    for i in range(N):
        dots[i].set_data([], [])
    return tuple(dots)

ani = animation.FuncAnimation(
    fig, update, frames=len(trajectories),
    init_func = init, blit = True, interval = 2
)
ani.save("Particle_Wave.mp4", fps=120, extra_args=['-vcodec', 'libx264'])


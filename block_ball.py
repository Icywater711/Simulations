import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

# constants
M = 10.0 # mass of the block
m = 7.0  # mass of the ball
dt = 0.01  # time step
steps = 1000  # number of time steps

# intial conditions
r =np.array([-3.0, 0.0]) # position of the block and ball respectively
v = np.array([10.0, 0.0])  # velocity of the block and ball respectively
N = np.array([[ M-m, -2*m],[2*M, M-m]])/(M+m)  # collision matrix
trajectories = []


for _ in range(steps):
    d = r[1]-r[0]  # distance between block and ball
    if v[0] > v[1] and d <=2:  # collision detection
        v = N @ v  # update velocities after collision

    if r[1] >= 20:  # ball hits the wall
        v[1] = -v[1]  # reverse ball velocity

    r += v*dt  # update positions
    if r[1]<= r[0]+2:  # prevent overlap
        r[1] = r[0]+2
    trajectories.append(r.copy())

trajectories = np.array(trajectories)

#animation setup
fig, ax = plt.subplots(figsize=(10,10), dpi=100)
ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
ax.set_aspect('equal')

block, = ax.plot([], [], 's', markersize=50, color='blue')
ball, = ax.plot([], [], 'o', markersize=8, color='red')

def update(frame):
    block.set_data([trajectories[frame, 0]], [0])
    ball.set_data([trajectories[frame, 1]], [0])
    return block, ball

def init():
    block.set_data([], [])
    ball.set_data([], [])
    return block, ball

ani = animation.FuncAnimation(fig, update, frames=steps, init_func=init, blit=True, interval=10)

ani.save("Block_Ball.mp4", fps=30, extra_args=['-vcodec', 'libx264'])


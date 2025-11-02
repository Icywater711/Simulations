import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
import math

# constants
M = 500.0 # mass of the block
m = 1.0  # mass of the ball
dt = 0.01  # time step
steps = 5000  # number of time steps
x = 2.5  # size of the block and ball

# intial conditions
r =np.array([-3.0, 0.0]) # position of the block and ball respectively
v = np.array([10.0, 0.0])  # velocity of the block and ball respectively
N = np.array([[ M-m, -2*m],[2*M, M-m]])/(M+m)  # collision matrix
trajectories = []


for _ in range(steps):

    d = r[1]-r[0]  # distance between block and ball

    if d <= x:  # collision detected
        v = N @ abs(v) 

    if d <= x and m*v[1] > M*v[0]: 
        v = N @ v
    
    if r[1] >= 19:  # ball hits the wall
        v[1] = -v[1]  # reverse ball velocity

    r += v*dt  # update positions
    if r[1]<= r[0]+x:  # prevent overlap
        r[1] = r[0]+x

    if r[1]>=19:  # prevent ball from going past wall
        r[1] = 19
    trajectories.append(r.copy())

trajectories = np.array(trajectories)

print("Total number of collisions:", math.floor(np.pi/4*np.sqrt(M/m)), 'collisions')
print("Closest approach of block to wall:", 19.0*np.sqrt(m/M), 'meters')

#animation setup
fig, ax = plt.subplots(figsize=(8,8), dpi=300)
ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor("black")
fig.patch.set_facecolor("black")

block, = ax.plot([], [], 's', markersize=50, color='blue')
ball, = ax.plot([], [], 'o', markersize=8, color='red')
line = ax.plot([19.5,19.5], [-20,20], color='white', linewidth=2)
def update(frame):
    block.set_data([trajectories[frame, 0]], [0])
    ball.set_data([trajectories[frame, 1]], [0])
    return block, ball

def init():
    block.set_data([], [])
    ball.set_data([], [])
    return block, ball

ani = animation.FuncAnimation(fig, update, frames=steps, init_func=init, blit=True, interval=10)

ani.save("Block_Ball.mp4", fps=120, extra_args=['-vcodec', 'libx264'])


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

#constants
k = 12000 # N m²/C², edited Coulomb's constant for better animation
masses = (1)  # masses in kg
dt = 0.002  # time step
steps = 1000  # number of time steps

charges = [
    [-1.75,[1.0, 0.0], [0.0, 1.0]],
    [-1.75, [-1.0, 0.0], [0.0, -1.0]],
    [1.75, [0.0, 1.0], [-1.0, 0.0]],
    [1.75, [0.0, -1.0], [1.0, 0.0]]
]
r=[]
v=[]
for i in range(len(charges)):
    r.append(10*np.array(charges[i][1]))
    v.append(20*np.array(charges[i][2]))    
r = np.array(r)
v = np.array(v)

F = np.empty_like(r)
trajectories = [r.copy()]

for _ in range(steps):
    F.fill(0.0)
    # calculate forces on each charge
    for i in range(len(charges)):
        for j in range(len(charges)):
            if i != j:
                r_ij = r[i]-r[j]
                d = np.linalg.norm(r_ij)
                if d < 1e-8:  # avoid singularity
                    d = 1e-8
                F[i] += k * charges[i][0] * charges[j][0] * r_ij / d**3
    
    v_half = v + 0.5 * F / masses * dt
    r += v_half * dt 
    F.fill(0.0)
    for i in range(len(charges)):
        for j in range(len(charges)):
            if i != j:
                r_ij = r[i]-r[j]
                d = np.linalg.norm(r_ij)
                if d < 1e-8:  # avoid singularity
                    d = 1e-8
                F[i] += k * charges[i][0] * charges[j][0] * r_ij / d**3
   
    v = v_half + 0.5 * F / masses * dt 
    trajectories.append(r.copy())


trajectories = np.array(trajectories) 

#animation setup
fig, ax = plt.subplots(figsize=(10,10), dpi=100)
ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor("black")
fig.patch.set_facecolor("black")

lines = [ax.plot([], [], lw=2)[0] for _ in range(len(charges))]
dots = []
for i in range(len(charges)):
    if charges[i][0] > 0:
        dot, = ax.plot([], [], 'o', color = 'red', markersize=8)
    else:
        dot, = ax.plot([], [], 'o', color = 'blue', markersize=8)
    dots.append(dot)

def update(frame):
    for i in range(len(charges)):
        lines[i].set_data(trajectories[:frame, i,0], trajectories[:frame, i, 1])
        dots[i].set_data([trajectories[frame, i, 0]], [trajectories[frame, i, 1]])
    return tuple(lines + dots)

def init():
    for i in range(len(charges)):
        lines[i].set_data([], [])
        dots[i].set_data([], [])
    return tuple( lines + dots)

ani = animation.FuncAnimation(
    fig, update, frames=len(trajectories),
    init_func = init, blit = True, interval = 2
)
ani.save("Electrodynamics.mp4", fps=60, extra_args=['-vcodec', 'libx264'])



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

#constants
g = 9.81 #m/s^2
m = 1 #kg
R = 1 #m
E = 100 #constant of motion
dt = 0.01 #s
steps = 1000

r= np.array([0.0,0.0]) #initial position
v = np.array([np.sqrt(2*E/m),0.0])
s= 1

trajectory =[r.copy()]

y =0
yp = 0

for _ in range(steps):
    #update position and velocity
    v = np.sqrt(2*(E/m-g*y)/(yp**2+1)) * np.array([1,yp])*s
    r += v*dt
    y = np.sin(r[0])
    yp = np.cos(r[0])
    
    if y >= (E/(m*g)) and s==1:
        s = -1
        r[0] = np.arcsin((E/(m*g)))
        yp = np.cos(r[0])
        y = np.sin(r[0])
        v= (1e-10)* np.array([1,yp])*s #to avoid numerical issues
        r += v*dt
        yp = np.cos(r[0])
        y = np.sin(r[0])

    if y >= (E/(m*g)) and s==-1:
        r[0]= -np.arcsin((E/(m*g)))
        yp = np.cos(r[0])
        y = np.sin(r[0])
        s= 1
        v= (1e-10)* np.array([1,yp])*s #to avoid numerical issues
        r += v*dt
        yp = np.cos(r[0])
        y = np.sin(r[0])

    trajectory.append(r.copy())

trajectory = np.array(trajectory)

#animation setup
fig, ax = plt.subplots()
ax.set_xlim(-20,20)
ax.set_ylim(-20,20)
ax.set_aspect('equal')
line, = ax.plot([], [], lw=2)
circle = plt.Circle((0, 0), R, color='r', fill=False)
ax.add_artist(circle)

def update(frame):
    line.set_data(trajectory[:frame, 0], trajectory[:frame, 1])
    circle.set_center((trajectory[frame, 0], trajectory[frame, 1]))
    return line, circle

def init():
    line.set_data([],[])
    circle.set_center((0,0))
    return line,circle

ani = animation.FuncAnimation(
    fig, update, frames=len(trajectory),
    init_func = init, blit = True, interval =20
)
ani.save("Particle_On_Parabola.mp4", fps=60, extra_args=['-vcodec', 'libx264'])








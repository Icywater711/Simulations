import matplotlib.pyplot as plt
import numpy as np

# Parameters
U = 1.0  # Velocity of the sphere
R = 1.0
N = 200  # Number of grid points in each direction
x = np.linspace(-3, 3, N)
y = np.linspace(-3,3, N)
X, Y =  np.meshgrid(x,y)

# Calculate the velocity field
r2 = X**2 +Y**2
r2[r2 < 1e-8] = 0.01   # Avoid division by zero inside the sphere
u = U * (1+ R**2*(Y**2 -X**2)/r2**2)
v = -2*R**2*U*X*Y/r2**2
V = np.sqrt(u**2 + v**2)

# Plotting
fig, ax = plt.subplots(figsize=(7,7))
ax.axis('off')

mask = r2 < R**2
v=np.ma.array(v, mask = mask)
u=np.ma.array(u, mask = mask)


ax.streamplot(
    X,Y,
    u,v,
    color = V**3,
    cmap = "inferno",
    linewidth = 1,
    density = 3,
    arrowstyle = '->',
    arrowsize = 0.5,
    integration_direction = 'both'

)
# Plot the sphere
circle = plt.Circle((0,0), R, color='Blue')
ax.add_artist(circle)
ax.set_aspect('equal')

plt.savefig('moving_sphere.png', dpi = 1000, bbox_inches='tight')
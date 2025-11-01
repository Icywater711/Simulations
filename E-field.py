import numpy as np
import matplotlib.pyplot as plt

#constants
k = 8.99e9  # N m^2/C^2, Coulomb's constant

#array of charges and their postions
charges = [
   
    (1,0,1),
    (-0.5,0,-2),
]

nx,ny =200,200
x = np.linspace(-3,3,nx)
y = np.linspace(-3,3,ny)
X,Y = np.meshgrid(x,y)

Ex = np.zeros(X.shape) # x-component of the electric field
Ey = np.zeros(Y.shape) # y-component of the electric field
V = np.zeros(X.shape)  # electric potential
for (dx, dy, q) in charges:
    #calculate the electric field vector components
    rx = X-dx
    ry =Y-dy
    r = np.sqrt(rx**2 + ry**2)
    Ex +=k*q*rx/r**3
    Ey +=k*q*ry/r**3
    V+=k*q/r

E = np.sqrt(Ex**2 + Ey**2) #magnitude of the electric field

fig,ax = plt.subplots(figsize=(7,7))
ax.axis('off')

ax.streamplot(
    X,Y,
    Ex,Ey,
    color = np.log(E),
    linewidth=1,
    cmap='inferno',
    density=3,
    arrowstyle='->',
    arrowsize= 0.1,integration_direction='both'
    )

V = np.ma.masked_where(V>1e10, V)
V = np.ma.masked_where(V<-1e10, V)

Contour = ax.contour(X,Y, V, 30, colors ='red', alpha=1.0, linewidths=1.5)
#plot the charges
for (dx, dy, q) in charges:
    if q>0:
        ax.plot(dx,dy,'ro',markersize=10)
    else:
        ax.plot(dx,dy,'bo',markersize=10)

ax.set_aspect('equal')

plt.savefig('E-field.png',dpi=500, bbox_inches='tight')


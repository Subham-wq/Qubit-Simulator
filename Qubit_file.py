import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Qubit state
# -----------------------------
def qubit(theta, phi):
    return np.array([
        np.cos(theta / 2),
        np.exp(1j * phi) * np.sin(theta / 2)
    ], dtype=complex)

# -----------------------------
# Apply unitary gate
# -----------------------------
def apply_gate(psi, U):
    return U @ psi

# -----------------------------
# General SU(2) gate
# -----------------------------
def SU2(alpha, beta, gamma):
    return np.array([
        [np.exp(-1j * (alpha + gamma) / 2) * np.cos(beta / 2),
         -np.exp(-1j * (alpha - gamma) / 2) * np.sin(beta / 2)],

        [np.exp(1j * (alpha - gamma) / 2) * np.sin(beta / 2),
         np.exp(1j * (alpha + gamma) / 2) * np.cos(beta / 2)]
    ], dtype=complex)

# Pauli matrices
sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)

# Bloch vector
def bloch_vector(psi):
    rho = np.outer(psi, np.conj(psi))
    x = np.real(np.trace(rho @ sx))
    y = np.real(np.trace(rho @ sy))
    z = np.real(np.trace(rho @ sz))
    return np.array([x, y, z])

# -----------------------------
# USER INPUT
# -----------------------------
theta = float(input("Enter theta (radians): "))
phi = float(input("Enter phi (radians): "))

alpha = float(input("Enter alpha (radians): "))
beta = float(input("Enter beta (radians): "))
gamma = float(input("Enter gamma (radians): "))

# Initial state
psi = qubit(theta, phi)

# Apply gate
psi = apply_gate(psi, SU2(alpha, beta, gamma))

# Bloch vector
vx, vy, vz = bloch_vector(psi)

# -----------------------------
# Plot Bloch sphere
# -----------------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color="lightblue", alpha=0.3)

t = np.linspace(0, 2*np.pi, 200)
ax.plot(np.cos(t), np.sin(t), 0, color='gray')

ax.plot([0,1],[0,0],[0,0], color='black')
ax.plot([0,0],[0,1],[0,0], color='black')
ax.plot([0,0],[0,0],[0,1], color='black')

ax.text(0,0,1.1,'|0>')
ax.text(0,0,-1.2,'|1>')
ax.text(1.1,0,0,'X')
ax.text(0,1.1,0,'Y')

ax.quiver(0,0,0,vx,vy,vz,color='red',linewidth=2)

ax.view_init(elev=25, azim=35)
ax.set_box_aspect([1,1,1])
ax.set_axis_off()

plt.show()

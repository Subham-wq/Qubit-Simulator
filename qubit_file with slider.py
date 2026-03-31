import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# -----------------------------
# Qubit state
# -----------------------------
def qubit(theta, phi):
    return np.array([
        np.cos(theta / 2),
        np.exp(1j * phi) * np.sin(theta / 2)
    ], dtype=complex)

# Apply gate
def apply_gate(psi, U):
    return U @ psi

# SU(2)
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
# Plot setup
# -----------------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.35)

# Sphere
u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
xs = np.cos(u)*np.sin(v)
ys = np.sin(u)*np.sin(v)
zs = np.cos(v)
ax.plot_wireframe(xs, ys, zs, color="lightblue", alpha=0.3)

# Equator
t = np.linspace(0, 2*np.pi, 200)
ax.plot(np.cos(t), np.sin(t), 0, color='gray')

# Axis labels
ax.text(0,0,1.1,'|0>')
ax.text(0,0,-1.2,'|1>')
ax.text(1.1,0,0,'X')
ax.text(0,1.1,0,'Y')

ax.set_box_aspect([1,1,1])
ax.set_axis_off()
ax.view_init(elev=25, azim=35)

# Initial vector
arrow = ax.quiver(0,0,0,1,0,0,color='red')

# -----------------------------
# Sliders
# -----------------------------
ax_theta = plt.axes([0.2, 0.25, 0.6, 0.02])
ax_phi   = plt.axes([0.2, 0.22, 0.6, 0.02])
ax_alpha = plt.axes([0.2, 0.18, 0.6, 0.02])
ax_beta  = plt.axes([0.2, 0.15, 0.6, 0.02])
ax_gamma = plt.axes([0.2, 0.12, 0.6, 0.02])

s_theta = Slider(ax_theta, 'theta', 0, 2*np.pi, valinit=1)
s_phi   = Slider(ax_phi,   'phi',   0, 2*np.pi, valinit=0)
s_alpha = Slider(ax_alpha, 'alpha', 0, 2*np.pi, valinit=0)
s_beta  = Slider(ax_beta,  'beta',  0, 2*np.pi, valinit=0)
s_gamma = Slider(ax_gamma, 'gamma', 0, 2*np.pi, valinit=0)

# -----------------------------
# Update function
# -----------------------------
def update(val):
    global arrow
    arrow.remove()

    theta = s_theta.val
    phi   = s_phi.val
    alpha = s_alpha.val
    beta  = s_beta.val
    gamma = s_gamma.val

    psi = qubit(theta, phi)
    psi = apply_gate(psi, SU2(alpha, beta, gamma))

    vx, vy, vz = bloch_vector(psi)

    arrow = ax.quiver(0,0,0,vx,vy,vz,color='red')
    fig.canvas.draw_idle()

s_theta.on_changed(update)
s_phi.on_changed(update)
s_alpha.on_changed(update)
s_beta.on_changed(update)
s_gamma.on_changed(update)

plt.show()
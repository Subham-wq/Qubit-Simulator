import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Qubit state
def qubit(theta, phi):
    return np.array([
        np.cos(theta / 2),
        np.exp(1j * phi) * np.sin(theta / 2)
    ], dtype=complex)

# SU(2)
def SU2(alpha, beta, gamma):
    return np.array([
        [np.exp(-1j * (alpha + gamma) / 2) * np.cos(beta / 2),
         -np.exp(-1j * (alpha - gamma) / 2) * np.sin(beta / 2)],
        [np.exp(1j * (alpha - gamma) / 2) * np.sin(beta / 2),
         np.exp(1j * (alpha + gamma) / 2) * np.cos(beta / 2)]
    ], dtype=complex)

def apply_gate(psi, U):
    return U @ psi

# Pauli matrices
sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)

def bloch_vector(psi):
    rho = np.outer(psi, np.conj(psi))
    x = np.real(np.trace(rho @ sx))
    y = np.real(np.trace(rho @ sy))
    z = np.real(np.trace(rho @ sz))
    return x, y, z

# ---------------- UI ----------------
st.title("Qubit Bloch Sphere Simulator")

theta = st.slider("Theta", 0.0, 2*np.pi, 1.0)
phi   = st.slider("Phi",   0.0, 2*np.pi, 0.0)

alpha = st.slider("Alpha", 0.0, 2*np.pi, 0.0)
beta  = st.slider("Beta",  0.0, 2*np.pi, 0.0)
gamma = st.slider("Gamma", 0.0, 2*np.pi, 0.0)

psi = qubit(theta, phi)
psi = apply_gate(psi, SU2(alpha, beta, gamma))

vx, vy, vz = bloch_vector(psi)

# Bloch sphere
u = np.linspace(0, 2*np.pi, 50)
v = np.linspace(0, np.pi, 25)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

fig = go.Figure()

fig.add_surface(x=x, y=y, z=z, opacity=0.2, showscale=False)

fig.add_trace(go.Scatter3d(
    x=[0, vx],
    y=[0, vy],
    z=[0, vz],
    mode='lines',
    line=dict(width=6)
))

fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-1,1]),
        yaxis=dict(range=[-1,1]),
        zaxis=dict(range=[-1,1])
    )
)

st.plotly_chart(fig)

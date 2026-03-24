import numpy as np
import matplotlib.pyplot as plt


#defining qubit

def qubit(theta, phi):
    psi = np.array([
        np.cos(theta / 2),
        np.exp(1j * phi) * np.sin(theta / 2)
    ], dtype=complex)

    return psi

psi = qubit(np.pi/2, 0)
print(psi)

#pauli matrices
sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)


def bloch_vector(psi):
    rho = np.outer(psi, np.conj(psi))

    x = np.real(np.trace(rho @ sx))
    y = np.real(np.trace(rho @ sy))
    z = np.real(np.trace(rho @ sz))

    return np.array([x, y, z])


vec = bloch_vector(psi)



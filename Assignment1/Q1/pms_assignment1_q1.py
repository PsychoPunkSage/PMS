# -*- coding: utf-8 -*-
"""PMS_Assignment1_Q1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SV4PzDeXjW8GkiGriQHrRm0vPq31fZnB

#**Question 1**

##Kt
"""

import numpy as np
import matplotlib.pyplot as plt

# Provided dataset
Temperature = [200, 273, 400, 600, 800, 1000, 1200]
ThermalConductivity = [403, 428, 420, 405, 389, 374, 358]

# Polynomial degree (adjustable based on the desired fit)
degree = 4

# Performing polynomial fit
coefficients = np.polyfit(Temperature, ThermalConductivity, degree)

# Evaluate the fitted polynomial
fitTemperature = np.linspace(min(Temperature), max(Temperature), 1000)
fitThermalConductivity = np.polyval(coefficients, fitTemperature)

# Plot the original data and the fitted polynomial
plt.figure()
plt.plot(Temperature, ThermalConductivity, 'o', label='Original Data')
plt.plot(fitTemperature, fitThermalConductivity, '-', label='Polynomial Fit')
plt.xlabel('Temperature (K)')
plt.ylabel('Thermal Conductivity (W/m-K)')
plt.legend(loc='best')
plt.title('Polynomial Fit to Thermal Conductivity Data')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# Displaying the coefficients of the fitted polynomial
print('\nPolynomial Coefficients:')
print(coefficients)

"""##Explicit Method"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
Cp = 235        # Specific heat capacity
rho = 10500     # Density
L = 1           # Length of the domain (1 cm)
T0 = 300.0      # Initial temperature
Tni = 300.0     # Neumann boundary condition
dx = 0.25       # Spatial step size

# Specify frequency of the sinusoidal boundary condition
# frequency = 1   # 1 Hz as an example
frequencies = [1, 10, 20, 30, 40]

for frequency in frequencies:
  # Calculate final time for at least 5 cycles
  num_cycles = 5
  final_time = num_cycles / frequency

  # Temporal parameters
  dt = 0.01       # Temporal step size
  num_steps = round(final_time / dt)  # Number of time steps

  # Initialize temperature array
  nx = round(L / dx) + 1
  T = np.ones((nx, num_steps)) * T0

  # Initialize stability flag
  stable = True

  # Function to calculate k(T) at each spatial and time step.
  def k(T):
      return -0.0024 * T**2 + 0.99 * T + 287.1191

  # Iterate through time steps
  for j in range(1, num_steps):
      # Update boundary conditions with a sinusoidal profile
      omega = 2 * np.pi * frequency
      T[0, j] = T0 * (1 + np.sin(omega * j * dt))
      T[-1, j] = Tni

      # Calculate temperature using explicit finite difference formula
      for i in range(1, nx-1):
          k_i = k(T[i, j-1])  # Evaluate k at the previous time step
          T[i, j] = T[i, j-1] + dt / Cp * k_i * (T[i+1, j-1] - 2*T[i, j-1] + T[i-1, j-1]) / dx**2

      # Check von Neumann stability criterion
      stability_condition = (np.max(k(T[:, j]) / (rho * Cp)) * dt) / dx**2
      if stability_condition >= 0.5:
          print(f"Stability criterion violated at time step {j}. Exiting.")
          stable = False
          break

  # Display results
  if stable:
      print(f"\n==============")
      print(f"Frequency {frequency}Hz")
      print(f"==============")
      print(f"Temperature at x=0.25L, t={final_time} = {T[int(round(0.25*L/dx)) + 1, -1]}")
      print(f"Temperature at x=0.50L, t={final_time} = {T[int(round(0.5*L/dx)) + 1, -1]}")
      print(f"Temperature at x=0.75L, t={final_time} = {T[int(round(0.75*L/dx)) + 1, -1]}")
      print(f"Temperature at x=1.00L, t={final_time} = {T[-1, -1]}")

      x_values = np.linspace(0, L, nx)
      plt.plot(x_values, T[:, -1])
      plt.title(f"Temperature Profile at t={final_time}")
      plt.xlabel('Position (x)')
      plt.ylabel('Temperature (T)')
      plt.grid(True)
      plt.show()

"""##Implicit Method"""

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.sparse import diags, eye
# from scipy.sparse.linalg import spsolve

# # Parameters
# Cp = 235          # Specific heat capacity
# rho = 10500       # Density
# L = 1             # Length of the domain (1 cm)
# T0 = 300.0        # Initial temperature
# Tni = 300.0       # Neumann boundary condition
# dx = 0.25         # Spatial step size

# # Specify frequency of the sinusoidal boundary condition
# frequency = 1     # 1 Hz as an example

# # Calculate final time for at least 5 cycles
# num_cycles = 5
# final_time = num_cycles / frequency

# # Temporal parameters
# dt = 0.01         # Temporal step size
# num_steps = round(final_time / dt)

# # Initialize temperature array
# nx = round(L / dx) + 1
# T = np.ones((nx - 1, num_steps)) * T0

# # Initialize stability flag
# stable = True

# # Function to calculate k(T) at each spatial and time step
# def k(T):
#     return -0.0024 * T**2 + 0.99 * T + 287.1191

# # Initialize coefficient matrix A using sparse matrix
# s = dt / (rho * Cp * dx**2)
# A = eye(nx - 1) - s * diags([-1, 2, -1], [-1, 0, 1], shape=(nx - 1, nx - 1))

# # Iterate through time steps
# for j in range(1, num_steps):
#     # Update boundary conditions with a sinusoidal profile
#     omega = 2 * np.pi * frequency
#     T[0, j] = T0 * (1 + np.sin(omega * j * dt))
#     T[-1, j] = Tni

#     # Evaluate thermal conductivity function k(T) at each spatial and time step
#     k_values = k(T[:, j-1])

#     # Construct right-hand-side vector b
#     b = T[:, j-1] + s * k_values

#     # Solve the system of equations using the backslash operator
#     T[:, j] = spsolve(A, b)

# # Display results
# print(f"Temperature at x=0.25L, t={final_time} = {T[int(round(0.25*L/dx)), -1]}")
# print(f"Temperature at x=0.50L, t={final_time} = {T[int(round(0.5*L/dx)), -1]}")
# print(f"Temperature at x=0.75L, t={final_time} = {T[int(round(0.75*L/dx)), -1]}")
# print(f"Temperature at x=1.00L, t={final_time} = {T[-1, -1]}")

# # Plot the final temperature profile
# x_values = np.linspace(0, L, nx - 1)
# plt.plot(x_values, np.vstack([T, Tni * np.ones(num_steps)]).T)
# plt.title(f"Temperature Profile at t={final_time}")
# plt.xlabel('Position (x)')
# plt.ylabel('Temperature (T)')
# plt.grid(True)
# plt.show()

"""##Crank-Nicholson Method"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

# Parameters
nx = 501          # Number of spatial points
nt = 501          # Number of time points

J = np.linspace(0, 1, nx)
L = np.linspace(0, 1, nt)

dx = 1 / (nx - 1)
dt = 1 / (nt - 1)

Cp = 1            # Specific heat
T0 = 300          # Initial temperature

# Frequency for the boundary condition
frequencies = [1, 10, 20, 30, 40]

for omega in frequencies:
  # Define the thermal conductivity function
  k = lambda T: -0.0024 * T**2 + 0.99 * T + 287.1191

  # Initialize arrays
  u = np.zeros((nt, nx))
  BCs = T0 * (1 + np.sin(2 * np.pi * omega * L))  # Updated boundary condition
  u0 = T0 * np.ones(nx)

  u[:, 0] = BCs
  u[:, -1] = T0  # Right-hand boundary always at 300K

  # Crank-Nicolson coefficients
  D = 1
  lbd = (D * dt) / (2 * dx**2)

  # Initialize tridiagonal matrices
  main_diag_A = 2 * (1 + lbd * k(u0[1:-1]))
  off_diag_A = -lbd * k(u0[1:-2])
  A = diags([main_diag_A, off_diag_A, off_diag_A], [0, 1, -1], (nx-2, nx-2)).toarray()

  main_diag_B = 2 * (1 - lbd * k(u0[1:-1]))
  off_diag_B = lbd * k(u0[1:-2])
  B = diags([main_diag_B, off_diag_B, off_diag_B], [0, 1, -1], (nx-2, nx-2)).toarray()

  # Time-stepping loop
  for n in range(nt - 1):
      b = u[n, 1:-1]

      # Include boundary conditions
      b[0] += lbd * k(u[n, 0]) * u[n, 0]
      b[-1] += lbd * k(u[n, -1]) * u[n, -1]

      b = B @ b
      sol = np.linalg.solve(A, b)
      u[n + 1, 1:-1] = sol

  # Indices corresponding to spatial locations
  idx_1 = round(0.25 * (nx - 1))
  idx_2 = round(0.5 * (nx - 1))
  idx_3 = round(0.75 * (nx - 1))
  idx_4 = nx - 1

  # Extract temperature values at specific spatial locations
  T_1 = u[:, idx_1]
  T_2 = u[:, idx_2]
  T_3 = u[:, idx_3]
  T_4 = u[:, idx_4]

  # Display the temperature profiles at different spatial locations
  print(f"\n==============")
  print(f"Frequency {omega}Hz")
  print(f"==============")
  print(f'Temperature at delta x = 0.25L: {T_1[-1]:.2f} K')
  print(f'Temperature at delta x = 0.5L: {T_2[-1]:.2f} K')
  print(f'Temperature at delta x = 0.75L: {T_3[-1]:.2f} K')
  print(f'Temperature at delta x = L: {T_4[-1]:.2f} K')

  # Plotting
  plt.figure()
  plt.title('Crank-Nicolson Method for 1-D Heat Conduction')
  plt.xlabel('x [-]')
  plt.ylabel('Temperature [K]')

  for n in range(0, nt, 50):
      plt.plot(np.linspace(0, 1, nx), u[n, :], label=f'Time = {n * dt:.2f} s')

  plt.legend()
  plt.grid(True)
  plt.show()

"""##Gauss Elimination"""

import numpy as np
import time

def gauss_elimination(X):
    nX, _ = X.shape
    for i in range(nX):
        if X[i, i] == 0:
            print('Diagonal element zero')
            return None
        X[i, :] = X[i, :] / X[i, i]
        for k in range(nX):
            if k == i:
                continue
            X[k, :] = X[k, :] - X[k, i] * X[i, :]
    return X

# Parameters
Cp = 235
T0 = 300.0
Tni = 300.0
L = 1
dx_values = [0.1, 0.01]  # Vary the spatial step sizes
omega = 1  # Frequency for boundary condition

# Time parameters
dt = 0.001  # Temporal step size
final_time = 1  # Final simulation time

# Function for k(T)
k = lambda T: -0.0024 * T**2 + 0.99 * T + 287.1191

# Initialize arrays for results
grid_points = np.zeros(len(dx_values))
computational_times = np.zeros(len(dx_values))

for dxi, dx in enumerate(dx_values):
    nx = round(L / dx) + 2

    # Initialize temperature matrix
    T = np.ones(nx) * T0

    # Time stepping loop
    start_time = time.time()  # Start timer
    for t in np.arange(dt, final_time + dt, dt):
        # Update boundary conditions
        omega_t = 2 * np.pi * omega * t
        T[0] = T0 * (1 + np.sin(omega_t))
        T[-1] = Tni

        # Construct tridiagonal matrix and solve using Gaussian elimination method
        A = np.diag(1 + 2 * dt / dx**2 * np.ones(nx - 2)) + np.diag(-dt / dx**2 * np.ones(nx - 3), 1) + np.diag(-dt / dx**2 * np.ones(nx - 3), -1)
        B = T[1:-1] + dt / 2 * (T[2:] - 2 * T[1:-1] + T[:-2])

        # Apply Gaussian elimination
        X = np.column_stack((A, B))
        X = gauss_elimination(X)

        # Update temperature values in the interior
        T[1:-1] = X[:, -1]

        # Save results at each time step if needed
        # (you can add your own code here if you want to save data)

    # Stop timer and record computational time
    computational_times[dxi] = time.time() - start_time

    # Save number of internal grid points
    grid_points[dxi] = nx - 2

# Display results
print('Spatial Step (dx) | Number of Internal Grid Points | Computational Time')
print('--------------------------------------------------------------------')
for i in range(len(dx_values)):
    print(f'{dx_values[i]:<20} {grid_points[i]:<30} {computational_times[i]:.6f}')

"""##Gauss-Jordan Elimination"""

import numpy as np
import time

def gauss_jordan_elim(A):
    n, m = A.shape
    A1 = np.copy(A)
    err = 0

    for i in range(n):
        A1[i:n, i:n + 1], err = gauss_pivot(A1[i:n, i:n + 1])
        if err == 0:
            A1[0:n, i:n + 1] = gauss_jordan_step(A1[0:n, i:n + 1], i)

    return A1, err

def gauss_jordan_step(A, i):
    n, m = A.shape
    A1 = np.copy(A)
    s = A1[i, 0]
    A1[i, :] = A[i, :] / s
    k = np.concatenate((np.arange(1, i), np.arange(i + 1, n)))
    for j in k:
        s = A1[j, 0]
        A1[j, :] = A1[j, :] - A1[i, :] * s

    return A1

def gauss_pivot(A):
    n, m = A.shape
    A1 = np.copy(A)
    err = 0

    if A1[0, 0] == 0:
        check = True
        i = 0
        while check:
            i += 1
            if i >= n:
                print('error: matrix is singular')
                err = 1
                check = False
            else:
                if A[i, 0] != 0 and check:
                    check = False
                    b = np.copy(A1[i, :])
                    A1[i, :] = np.copy(A1[0, :])
                    A1[0, :] = np.copy(b)

    return A1, err

# Parameters
Cp = 235
T0 = 300.0
Tni = 300.0
L = 1
dx_values = [0.1, 0.01]  # Vary the spatial step sizes
omega = 1  # Frequency for boundary condition

# Time parameters
dt = 0.001  # Temporal step size
final_time = 1  # Final simulation time

# Function for k(T)
k = lambda T: -0.0024 * T**2 + 0.99 * T + 287.1191

# Initialize arrays for results
grid_points = np.zeros(len(dx_values))
computational_times = np.zeros(len(dx_values))

for dxi, dx in enumerate(dx_values):
    nx = round(L / dx) + 2

    # Initialize temperature matrix
    T = np.ones((nx, 1)) * T0

    # Time stepping loop
    start_time = time.time()  # Start timer
    for t in np.arange(dt, final_time + dt, dt):
        # Update boundary conditions
        omega_t = 2 * np.pi * omega * t
        T[0] = T0 * (1 + np.sin(omega_t))
        T[-1] = Tni

        # Construct tridiagonal matrix and solve using Gauss-Jordan elimination method
        A = np.diag(1 + 2 * dt / dx**2 * np.ones(nx-2)) + np.diag(-dt / dx**2 * np.ones(nx-3), 1) + np.diag(-dt / dx**2 * np.ones(nx-3), -1)
        B = T[1:-1] + dt/2 * (T[2:] - 2 * T[1:-1] + T[:-2])

        # Augmenting matrix A with vector B
        Aa = np.column_stack((A, B))

        # Apply Gauss-Jordan elimination
        Aa, err = gauss_jordan_elim(Aa)

        # Update temperature values in the interior
        T[1:-1] = Aa[:, -1].reshape(-1, 1)

        # Save results at each time step if needed
        # (you can add your own code here if you want to save data)

    # Stop timer and record computational time
    computational_times[dxi] = time.time() - start_time

    # Save number of internal grid points
    grid_points[dxi] = nx - 2

# Display results
print('Spatial Step (dx) | Number of Internal Grid Points | Computational Time')
print('--------------------------------------------------------------------')
for i in range(len(dx_values)):
    print(f'{dx_values[i]:<20} {grid_points[i]:<30} {computational_times[i]:.6f}')

"""##Thomas Algorithm"""

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
import time

# Parameters
Cp = 235
T0 = 300.0
Tni = 300.0
L = 1
dx_values = [0.1, 0.01, 0.001, 0.00001]  # Vary the spatial step sizes
omega = 1  # Frequency for boundary condition

# Time parameters
dt = 0.001  # Temporal step size
final_time = 1  # Final simulation time

# Function for k(T)
k = lambda T: -0.0024 * T**2 + 0.99 * T + 287.1191

# Initialize arrays for results
grid_points = np.zeros(len(dx_values))
computational_times = np.zeros(len(dx_values))

def thomas(mu, d, N):
    # Coefficients
    b = 1 + 2 * mu
    e = np.zeros(N)
    f = np.zeros(N)

    e[0] = mu / b
    f[0] = d[0] / b

    for j in range(1, N):
        den = 1 + (2 - e[j-1]) * mu
        e[j] = mu / den
        f[j] = (d[j] + mu * f[j-1]) / den

    # Back substitution
    u = np.zeros(N)
    u[-1] = f[-1]

    for j in range(N-2, -1, -1):
        u[j] = f[j] + e[j] * u[j+1]

    return u

for dxi, dx in enumerate(dx_values):
    nx = round(L / dx) + 2

    # Initialize temperature matrix
    T = np.ones(nx) * T0

    # Time stepping loop
    start_time = time.time()  # Start timer
    for t in np.arange(dt, final_time + dt, dt):
        # Update boundary conditions
        omega_t = 2 * np.pi * omega * t
        T[0] = T0 * (1 + np.sin(omega_t))
        T[-1] = Tni

        # Construct tridiagonal matrix and solve using Thomas algorithm
        mu = dt / dx**2
        A = diags([1 + 2 * mu, -mu, -mu], [0, 1, -1], shape=(nx-2, nx-2), format='csr')
        d = T[1:-1] + mu/2 * (T[2:] - 2 * T[1:-1] + T[:-2])

        # Solve tridiagonal system using Thomas algorithm
        u_interior = thomas(mu, d, nx-2)

        # Update temperature values in the interior
        T[1:-1] = u_interior

        # Save results at each time step if needed
        # (you can add your own code here if you want to save data)

    # Stop timer and record computational time
    computational_times[dxi] = time.time() - start_time

    # Save number of internal grid points
    grid_points[dxi] = nx - 2

# Display results
print('Spatial Step (dx) | Number of Internal Grid Points | Computational Time')
print('--------------------------------------------------------------------')
for i in range(len(dx_values)):
    print(f'{dx_values[i]:<20} {grid_points[i]:<30} {computational_times[i]:.6f}')

"""##Part::> f"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.integrate import trapz

# Parameters
Cp = 235
T0 = 300.0
Tni = 300.0
L = 1
dx_values = [0.1, 0.01, 0.001]  # Vary the spatial step sizes
omega_values = np.linspace(0, 10, 100)  # Vary the frequency

# Time parameters
dt = 0.001  # Temporal step size
final_time = 1  # Final simulation time

# Function for k(T)
k = lambda T: -0.0024 * T**2 + 0.99 * T + 287.1191

# Initialize arrays for results
grid_points = np.zeros(len(dx_values))
computational_times = np.zeros(len(dx_values))

def thomas(mu, d, N):
    # Coefficients
    b = 1 + 2 * mu
    e = np.zeros(N)
    f = np.zeros(N)

    e[0] = mu / b
    f[0] = d[0] / b

    for j in range(1, N):
        den = 1 + (2 - e[j-1]) * mu
        e[j] = mu / den
        f[j] = (d[j] + mu * f[j-1]) / den

    # Back substitution
    u = np.zeros(N)
    u[-1] = f[-1]

    for j in range(N-2, -1, -1):
        u[j] = f[j] + e[j] * u[j+1]

    return u

# Loop over different spatial step sizes
for dxi, dx in enumerate(dx_values):
    nx = round(L / dx) + 2

    # Initialize temperature matrix
    T = np.ones(nx) * T0

    # Initialize arrays for storing results at different omega values
    T_x0_values = np.zeros(len(omega_values))
    T_avg_t_values = np.zeros(len(omega_values))
    T_xL_values = np.zeros(len(omega_values))

    # Time stepping loop
    for t in np.arange(dt, final_time + dt, dt):
        # Loop over different omega values
        for omega_idx, omega in enumerate(omega_values):
            omega_t = 2 * np.pi * omega * t
            T[0] = T0 * (1 + np.sin(omega_t))

            # Construct tridiagonal matrix and solve using Thomas algorithm
            mu = dt / dx**2
            A = diags([1 + 2 * mu, -mu, -mu], [0, 1, -1], shape=(nx-2, nx-2), format='csr')
            d = T[1:-1] + mu/2 * (T[2:] - 2 * T[1:-1] + T[:-2])

            # Solve tridiagonal system using Thomas algorithm
            u_interior = thomas(mu, d, nx-2)

            # Update temperature values in the interior
            T[1:-1] = u_interior

            # Save results at each time step for each omega
            T_x0_values[omega_idx] = T[0]
            T_avg_t_values[omega_idx] = trapz(dx * np.arange(1, nx+1), T) / L
            T_xL_values[omega_idx] = T[-1]

        # Save results at each time step if needed
        # (you can add your own code here if you want to save data)

    # Save number of internal grid points
    grid_points[dxi] = nx - 2

    # Display results for each spatial step size
    print(f'Spatial Step (dx) = {dx}')
    print('--------------------------------------------------------------------')
    print(f'Number of Internal Grid Points: {nx - 2}')

    # Plot results for different omega values
    plt.figure()

    # Plot Temperature at x=0
    plt.subplot(3, 1, 1)
    plt.plot(omega_values, T_x0_values)
    plt.title('Temperature at x = 0')
    plt.xlabel('omega')
    plt.ylabel('T(x = 0, t)')

    # Plot Length-Averaged Temperature
    plt.subplot(3, 1, 2)
    plt.plot(omega_values, T_avg_t_values)
    plt.title('Length-Averaged Temperature')
    plt.xlabel('\omega')
    plt.ylabel('T_{avg}(t)')

    # Plot Temperature at x=L
    plt.subplot(3, 1, 3)
    plt.plot(omega_values, T_xL_values)
    plt.title('Temperature at x = L')
    plt.xlabel('\omega')
    plt.ylabel('T(x = L, t)')

    plt.tight_layout()
    plt.show()
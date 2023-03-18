# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:00:14 2023

@author: enriq
"""

# Cargamos el software anastruct
from anastruct import SystemElements
from anastruct import Cross_section
import pandas as pd
import numpy as np

# Definicion de variables
hft = 215.56
hw = 207.8
tw = 8
tf = 8

l1 = 1
l2 = 3

QP = -10
GD = 6.56

Ey = 2.1E+11
fck = 275

# Cargamos el objeto con nuestra sección
cs = Cross_section()

cs.pts = [(hft/2-tw/2, 0), (hft/2+tw/2, 0), (hft/2+tw/2, hw), (hft, hw), (hft, hw+tf), 
          (0, hw+tf), (0, hw), (hft/2-tw/2, hw)]
print(cs.calculate_section())
cs.plot('Section', size=(8, 6))


# Generamos la estructura
# Cargamos el objeto de nuestra estructura
ss = SystemElements()
# Añadimos elemento barra 1
ss.add_element(location=[[0, 0], [l1, 0]],EI=Ey*cs.Ixx*1E-12);
# Añadimos elemento barra 2
ss.add_element(location=[[l1, 0], [l1+l2, 0]],EI=Ey*cs.Ixx*1E-12);

# Añadimos apoyo fijo al nodo 1
ss.add_support_hinged(node_id=3)
# Añadimos apoyo fijo al nodo 2
ss.add_support_roll(node_id=2, direction=2)


# Añadimos carga puntual
ss.point_load(1, Fx=0.0, Fy=QP)
# Añadimos cargas distribuidas
ss.q_load(element_id=2, q=(GD,0), q_perp=(0,0))

# Mostramos estructura generada
ss.show_structure(title='Ejercicio 3')

# Resolvemos la estructura
ss.solve();

# Mostramos las reacciones
ss.show_reaction_force()

# Mostramos cortantes
#ss.show_shear_force()

# Mostramos flectores
# ss.show_bending_moment()

# Mostramos axiles
#ss.show_axial_force()

# Mostramos deformada
#ss.show_displacement(factor=6000)

resultados = ss.get_element_results(0)
resultados = pd.DataFrame(resultados)
Mdmax = np.max(np.array([resultados['Mmax'].abs().max(),resultados['Mmin'].abs().max()]))
Vdmax = np.max(np.array([resultados['Qmax'].abs().max(),resultados['Qmin'].abs().max()]))

print('Cortante máximo: '+str(Vdmax),' kN')
print('Flector máximo: '+str(Mdmax),' kNm')

# Mayoramos
Vdmax = Vdmax*1.35
Mdmax = Mdmax*1.35

Szmax = hft*tf*(hw+tf/2-cs.cy)+(hw-cs.cy)*tw*(hw-cs.cy)/2
Av = (hw+2*tf)*tw

# Navier
ymax = np.max(np.array([hw+2*tf-cs.cy,cs.cy]))
sigma_n = Mdmax*1E+6*ymax/cs.Ixx
print('Tension Navier: '+str(sigma_n)+' Mpa')
# Collignon
tau_col = Vdmax*1E+3*Szmax/(tw*cs.Ixx)
print('Tension Colignon: '+str(tau_col)+' Mpa')
# CTE
tau_CTE = Vdmax*1E+3/Av
print('Tension CTE: '+str(tau_CTE)+' Mpa')

# Von Mises
sigma_col = np.sqrt(sigma_n**2+3*tau_col**2)
print('Tension comparacion Collignon: '+str(sigma_col)+' Mpa')
sigma_CTE = np.sqrt(sigma_n**2+3*tau_CTE**2)
print('Tension comparacion CTE: '+str(sigma_CTE)+' Mpa')


# Comprobacion
fyd = fck/1.05
print('Comprobacion Collignon')
if sigma_col<fyd:
    print('NO PLASTIFICA!')
else:
    print('PLASTIFICA!')

print('Comprobacion CTE')
if sigma_CTE<fyd:
    print('NO PLASTIFICA!')
else:
    print('PLASTIFICA!')
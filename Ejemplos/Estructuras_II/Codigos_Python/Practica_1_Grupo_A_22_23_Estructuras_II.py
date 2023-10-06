# -*- coding: utf-8 -*-
"""Practica Coordinacion Grafica

ESTRUCTURAS II - Curso 2022/2023


"""

from sympy import SingularityFunction,symbols,Function,factorial,integrate
import matplotlib.pyplot as plt
import numpy as np
from sympy.plotting import plot
from sympy import init_printing
from sympy import *
from IPython.display import display, Math
from anastruct import Steel_profiles
import pandas as pd
import numpy as np
from anastruct import SystemElements
import collections
collections.Iterable = collections.abc.Iterable


cross_section = Steel_profiles()
sel_profile = cross_section.IPE_profiles[cross_section.IPE_profiles['Perfil'] == 'IPE-180']
I = float(sel_profile['Iy']*1E-8)
Wy = float(sel_profile['Wy']*1E+3)
A = float(sel_profile['A']*1E+2)
hp = float(sel_profile['h'])
tw = float(sel_profile['tw'])
Av = hp*tw
EI = 2.1E+11*I
La = 5.0
Lb = 2.0

g_G = 1.35
g_Q = 1.50

#g_G = 1.00
#g_Q = 1.00

PF = 4000.*g_G
CMS = 1000.*g_G
SU = 2000.*g_Q
Q = PF+CMS+SU
print('Carga por unidad de superficie: '+str(Q/1000.)+ ' kN/m2')

qac = 7000.*g_G
qab = Q*1.60/2.0

ca = qab*5+qac*7
cb = qab*5**2/2+qac*7**2/2
cc = (qac+qab)*5**3
cd = (qac+qab)*7**4-qab*2**4
A = np.array([[1,1,1,0],
              [0,5,7,0],
              [4*5**2,0,0,4*3*2],
              [4*7**3,4*2**3,0,7*4*3*2]])
np.matmul(np.linalg.inv(A),np.array([[ca/1000],[cb/1000],[cc/1000],[cd/1000]]))

ss = SystemElements(mesh=200)

# Añadimos elementos
ss.add_element(location=[[0.0, 0.0], [La,0.0]], EI = EI)
ss.add_element(location=[[La, 0.0], [La+Lb,0.0]], EI = EI)

# Añadimos cargas
ss.q_load(element_id=1,  q=(qac+qab,qac+qab))
ss.q_load(element_id=2,  q=(qac,qac))

# Añadimos condiciones de borde
ss.add_support_hinged(node_id=1)
ss.add_support_hinged(node_id=2)       
ss.add_support_hinged(node_id=3)  

# Mostramos estructura generada
ss.show_structure()

# Resolvemos la estructura
ss.solve()
#ss.optimize(profile_type='IPE', fyd = 275/1.05)

# Mostramos las reacciones
ss.show_reaction_force()

# Mostramos flectores
ss.show_bending_moment()


# Mostramos cortantes
ss.show_shear_force()

ss.show_displacement(factor = 100)

resultados = ss.get_element_results(0)
resultados = pd.DataFrame(resultados)
Mdmax = 1000*np.max(np.array([resultados['Mmax'].abs().max(),resultados['Mmin'].abs().max()])) 
Vdmax = np.max(np.array([resultados['Qmax'].abs().max(),resultados['Qmin'].abs().max()])) 
dispv = np.max(np.array([resultados['umax'].abs().max(),resultados['umin'].abs().max()])) 
disph = np.max(np.array([resultados['wmax'].abs().max(),resultados['wmin'].abs().max()])) 
sigma_n = Mdmax/Wy
tau = Vdmax/Av
von_mises = np.sqrt(sigma_n**2+3*tau**2)

print('Mmax = '+str(Mdmax))
print('Vdmax = '+str(Vdmax))
print('Sigma_n = '+str(sigma_n))
print('tau = '+str(tau))
print('Sigma_co = '+str(von_mises))
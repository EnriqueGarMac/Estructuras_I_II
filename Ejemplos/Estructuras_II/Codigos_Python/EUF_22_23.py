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
sel_profile = cross_section.IPE_profiles[cross_section.IPE_profiles['Perfil'] == 'IPE-120']
I = float(sel_profile['Iy']*1E-8)
Wy = float(sel_profile['Wy']*1E+3)
A = float(sel_profile['A']*1E+2)
hp = float(sel_profile['h'])
tw = float(sel_profile['tw'])
Av = hp*tw
EI = 2.1E+11*I

h = np.sqrt(7**2-(5.4-4)**2)
sinalph = h/7.0

g_G = 1.35
g_Q = 1.50

#g_G = 1.00
#g_Q = 1.00

PF = 4000.*g_G
CMS = 1000.*g_G
SU = 2000.*g_Q
Q = PF+CMS+SU
print('Carga por unidad de superficie: '+str(Q/1000.)+ ' kN/m2')

qa = Q*5.4*sinalph/2
qb = Q*4*sinalph/2

ca = 7*qb+(qa-qb)*7/2
cb = qb*7**2/2+(qa-qb)*7**2/6
cc = -7**2*0.25*(-qa+(qa-qb)/5)
A = np.array([[1,1,0],
              [0,7,1],
              [7,0,-3]])
np.matmul(np.linalg.inv(A),np.array([[ca/1000],[cb/1000],[cc/1000]]))

ss = SystemElements(mesh=1600)

# Añadimos elementos
ss.add_element(location=[[0.0, 0.0], [4.,0.0]], EI = EI)
ss.add_element(location=[[4.0, 0.0], [8.,0.0]], EI = EI)

# Añadimos cargas
ss.q_load(element_id=1,  q=(15,0))
ss.q_load(element_id=2,  q=(0,15))
ss.moment_load(2, Ty=40)

# Añadimos condiciones de borde
ss.add_support_hinged(node_id=1)
ss.add_support_hinged(node_id=2)         
ss.add_support_hinged(node_id=3)    

# Mostramos estructura generada
ss.show_structure()

# Resolvemos la estructura
ss.solve()
ss.optimize(profile_type='IPE', fyd = 275/1.05)

# Mostramos las reacciones
ss.show_reaction_force()

# Mostramos flectores
ss.show_bending_moment()


# Mostramos cortantes
ss.show_shear_force()

ss.show_displacement(factor = 10000)

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
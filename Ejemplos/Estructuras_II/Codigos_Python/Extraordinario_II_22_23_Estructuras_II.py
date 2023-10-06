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
import math
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


ca = 45
cb = 20
cc = 6.75
A = np.array([[1.,1.,0],
              [0,3.,1.],
              [0.5,0.,-0.5]])
sol = np.matmul(np.linalg.inv(A),np.array([[ca],[cb],[cc]]))
Ra = sol[0][0]
Rb = sol[1][0]
Ma = sol[2][0]
-Ma*6**2/2+Ra*6**3/6+Rb*3**3/6-20*(6**4-3**4)/(4*3*2)+10*(6**5-3**5)/(3*5*4*3*2)-10*3**4/(4*3*2)
293.6250000000002/(2.1*2*364)
-Ma+Ra*3-10*9+5*3**3/9
Ra-60+15

ss = SystemElements(mesh=1600)

# Añadimos elementos
ss.add_element(location=[[0.0, 0.0], [3.,0.0]], EI = EI)
ss.add_element(location=[[3.0, 0.0], [6.,0.0]], EI = EI)

# Añadimos cargas
gamma = 1.
ss.q_load(element_id=1,  q=(gamma*20,gamma*10))
ss.moment_load(3, -40*gamma)

# Añadimos condiciones de borde
ss.add_support_fixed(node_id=1)
ss.add_support_hinged(node_id=2)         

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

ss.show_displacement(factor = 5)

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


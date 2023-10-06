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
from anastruct import Cross_section
import collections
collections.Iterable = collections.abc.Iterable


# Cargamos el objeto con nuestra sección
cs = Cross_section()


cross_section = Steel_profiles()
sel_profile = cross_section.IPE_profiles[cross_section.IPE_profiles['Perfil'] == 'IPE-550']
I = float(sel_profile['Iy']*1E-8)
Wy = float(sel_profile['Wy']*1E+3)
A = float(sel_profile['A']*1E+2)
hp = float(sel_profile['h'])
tw = float(sel_profile['tw'])
Av = hp*tw
EI = 2.1E+11*I

ss = SystemElements(mesh=1600)

# Añadimos elementos
ss.add_element(location=[[0.0, 0.0], [1.0,0.0]], EI = 1)
ss.add_element(location=[[1.0, 0.0], [7.0,0.0]], EI = 1)
ss.add_element(location=[[7.0, 0.0], [8.0,0.0]], EI = 1)

# Añadimos cargas
ss.q_load(element_id=2,  q=(70*1000,0))


# Añadimos condiciones de borde
ss.add_support_fixed(node_id=1)               
ss.add_support_hinged(node_id=4)         

ss.point_load(3, Fx=0, Fy=-265*1000)

# Mostramos estructura generada
ss.show_structure()

# Resolvemos la estructura
ss.solve()
#ss.optimize(profile_type='IPE', fyd = 275/1.05, ELS = L/400)
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



Ra = float(Asol[0])
Rb = float(Asol[1])
Rc = float(Asol[2])
C1 = float(Asol[3])

x = 1.27
Ra*x**3/(6)-qa*x**4/(1000*4*3*2)-qb*x**4/(1000*4*3*2)+qb*x**5/(1000*6*5*4*3*2)+C1*x
x = 4.5
Ra*x**3/(6)+Rb*(x-3)**3/(6)-Fd*(x-4.5)**3/6000-qa*(x**4-(x-3)**4)/(1000*4*3*2)-qb*x**4/(1000*4*3*2)+qb*x**5/(1000*6*5*4*3*2)+C1*x
x = 4.7
Ra*x**3/(6)+Rb*(x-3)**3/(6)-Fd*(x-4.5)**3/6000-qa*(x**4-(x-3)**4)/(1000*4*3*2)-qb*x**4/(1000*4*3*2)+qb*x**5/(1000*6*5*4*3*2)+C1*x











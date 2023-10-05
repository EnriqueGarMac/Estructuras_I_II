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

cross_section = Steel_profiles()
sel_profile = cross_section.IPE_profiles[cross_section.IPE_profiles['Perfil'] == 'IPE-180']
I = float(sel_profile['Iy']*1E-8)
Wy = float(sel_profile['Wy']*1E+3)
A = float(sel_profile['A']*1E+2)
hp = float(sel_profile['h'])
tw = float(sel_profile['tw'])
Av = hp*tw
EI = 2.1E+11*I

Qk = 3 + 3 
Qd = 3*1.35 + 3*1.5
Qk = Qk*1000
Qd = Qd*1000
gammaf = Qd/Qk
gammaf = 1.0

print('Combinacion caracteristica: '+str(Qk)+ ' kN/m2')
print('Combinacion de diseño: '+str(Qd)+ ' kN/m2')
print('Ratio: '+str(gammaf))

q1 = Qk*3/2
ca = Qk*8+2.*2.*q1
cb = 4.*2.*q1/3.+32.*Qk+(4.+2.*4/3.)*2.*q1
cc = -(Qk+q1)*4.**4/math.factorial(4)+q1*4.**5/(4.*math.factorial(5))
cd = -(Qk+q1)*8.**4/math.factorial(4)+q1*8.**5/(4.*math.factorial(5))-q1*4.**5/(2.*math.factorial(5))
A = np.array([[1.,1.,1.,0],
              [0,4.,8.,0],
              [4.**3/6.,0,0,4.],
              [8.**3/6.,4.**3/6.,0,8.]])
np.matmul(np.linalg.inv(A),np.array([[ca],[cb],[-cc],[-cd]]))

ss = SystemElements(mesh=1600)

# Añadimos elementos
ss.add_element(location=[[0.0, 0.0], [4.,0.0]], EI = EI)
ss.add_element(location=[[4.0, 0.0], [8.,0.0]], EI = EI)

# Añadimos cargas
Qk = Qk*gammaf
q1 = q1*gammaf
ss.q_load(element_id=1,  q=(Qk+q1,Qk))
ss.q_load(element_id=2,  q=(Qk,Qk+q1))

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

ss.show_displacement(factor = 50)

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


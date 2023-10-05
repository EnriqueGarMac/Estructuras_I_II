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

# Cargamos el objeto con nuestra sección
cs = Cross_section()

hfb =  80
hft = 80
tw = 5
tf = 8
hw = 300-2*tf
cs.pts = [(0, 0), (hfb, 0), (hfb, tf), (hfb/2+tw/2, tf), (hfb/2+tw/2, tf+hw), 
          (hfb/2+hft/2, tf+hw), (hfb/2+hft/2, tf+hw+tf), (hfb/2-hft/2, tf+hw+tf),
          (hfb/2-hft/2, tf+hw),(hfb/2-tw/2, tf+hw),(hfb/2-tw/2, tf),(0, tf)]
print(cs.calculate_section())
cs.plot('Section', size=(8, 6))
Av = 170*tw

cross_section = Steel_profiles()
sel_profile = cross_section.IPE_profiles[cross_section.IPE_profiles['Perfil'] == 'IPE-300']
I = float(sel_profile['Iy']*1E-8)
Wy = float(sel_profile['Wy']*1E+3)
A = float(sel_profile['A']*1E+2)
hp = float(sel_profile['h'])
tw = float(sel_profile['tw'])
Av = hp*tw

EI = 2.1E+11*cs.Ixx*1E-12
Wy = cs.Ixx/(170/2)
#EI = 2.1E+11*I

hs = 4.0
hinf = 3
L = 3.0

g_G = 1.35
g_Q = 1.50

#g_G = 1.00
#g_Q = 1.00

PF = 4000.*g_G
SU = 2000.*g_Q
Q = PF+SU
print('Carga por unidad de superficie: '+str(Q/1000.)+ ' kN/m2')

qa = Q*hinf/2
qb = Q*hs/2

Fd = Q*3*3/2
ca = 3*qa+qb*3+Fd
cb = qa*3**2/2+qb*6+4.5*Fd
cc = 3*(qa+qb)/4-qb*3/(5*4*2)
cd = Fd*1.5**3/6+qa*(6**4-3**4)/(4*3*2)+qb*6**4/(4*3*2)-qb*6**5/(6*5*4*3*2)
cd = Fd/2**4+3*qa*(2**4-1)/2**3+24*qb/5
A = np.array([[1,1,1,0],
              [0,3,6,0],
              [1,0,0,2/3],
              [6**3/(3*2),3**3/6,0,6]])
A = np.array([[1,1,1,0],
              [0,3,6,0],
              [1,0,0,2/3],
              [4,0.5,0,2/3]])
np.matmul(np.linalg.inv(A),np.array([[ca/1000],[cb/1000],[cc/1000],[cd/1000]]))

ss = SystemElements(mesh=1600)

# Añadimos elementos
ss.add_element(location=[[0.0, 0.0], [L,0.0]], EI = EI)
ss.add_element(location=[[L, 0.0], [2*L,0.0]], EI = EI)

# Añadimos cargas
ss.q_load(element_id=1,  q=(qa+qb,qa+qb/2))
ss.q_load(element_id=2,  q=(qb/2,0))

# Añadimos condiciones de borde
ss.add_support_fixed(node_id=1)         
ss.add_support_hinged(node_id=3)         

ss.point_load(2, Fx=0, Fy=-Q*L*hinf/2)

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
# -*- coding: utf-8 -*-
"""Practica_EDE_Hiperestatica.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zK0wWTpvqgiZc6VnGNwniARSLF4hWQnV

**EDE - Viga hiperestática**
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


ss = SystemElements(mesh=12)

# Añadimos elementos
ss.add_element(location=[[0.0, 0.0], [2.5,0.0]])
ss.add_element(location=[[2.5, 0.0], [5.0,0.0]])

# Añadimos cargas
ss.q_load(element_id=1,  q=(0,5700))
ss.q_load(element_id=2,  q=(5700,0))

# Añadimos condiciones de borde
ss.add_support_hinged(node_id=1)
ss.add_support_roll(node_id=3, direction=2)


# Mostramos estructura generada
ss.show_structure()

# Resolvemos la estructura
#ss.solve()
ss.optimize(profile_type='IPN', fyd = 275/1.05, ELS = 5.0/400)

# Mostramos las reacciones
ss.show_reaction_force()

# Mostramos flectores
ss.show_bending_moment(factor = 0.0001)


# Mostramos cortantes
ss.show_shear_force()

ss.show_displacement(factor = 100)

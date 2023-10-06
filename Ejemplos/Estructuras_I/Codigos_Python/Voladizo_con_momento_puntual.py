# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements
import collections
collections.Iterable = collections.abc.Iterable

ss = SystemElements()

L = 3.0  # Longitud de la barra
M = -20.0 # Momento puntual

# Añadimos elemento barra 1
ss.add_element(location=[[0, 0], [L, 0]])


# Añadimos empotramiento al nodo 1
ss.add_support_fixed(node_id=1)

# Añadimos momento puntual al nodo 2
ss.moment_load(2, Ty=M)

# Mostramos estructura generada
ss.show_structure(title='Viga en voladizo con momento puntual')

# Resolvemos la estructura
ss.solve()

# Mostramos las reacciones
ss.show_reaction_force()

# Mostramos cortantes
ss.show_shear_force()

# Mostramos flectores
ss.show_bending_moment()

# Mostramos axiles
ss.show_axial_force()

# Mostramos deformada
ss.show_displacement()

# Mostramos todos los resultados juntos
ss.plotter.results_plot()

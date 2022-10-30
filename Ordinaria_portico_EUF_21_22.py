# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements

ss = SystemElements()

# Añadimos cordones inferiores
ss.add_element(location=[[0,0], [0,6]])
ss.add_element(location=[[0,6], [2,6]], spring={2: 0})
ss.add_element(location=[[2,6], [3,6]])
ss.add_element(location=[[3,6], [4,6]])
ss.add_element(location=[[4,6], [4,2]])

# BCs
ss.add_support_roll(node_id=6, direction=2)
ss.add_support_fixed(node_id=1)

# Añadimos carga puntual al nodo 2
ss.point_load(4, Fy=-10)
ss.q_load(element_id=1, q=(6,0))
ss.q_load(element_id=5, q=(4,4))

# Mostramos estructura generada
ss.show_structure(title='Problema 1 ordinaria ')

# Resolvemos la estructura
ss.solve()

# Mostramos las reacciones
ss.show_reaction_force()


# Mostramos axiles
ss.show_axial_force()

# Mostramos flectores
ss.show_bending_moment()

# Mostramos cortantes
ss.show_shear_force()

# Mostramos deformada
ss.show_displacement()

# Mostramos todos los resultados juntos
#ss.plotter.results_plot()

ss.printdispl()
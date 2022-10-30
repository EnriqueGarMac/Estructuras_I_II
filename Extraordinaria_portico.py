# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements

ss = SystemElements()

base_l = 1.0
Linc = np.sqrt(1.**2+2.**2)
cosa = base_l/Linc
sina = 2./Linc
ptot = 10.*base_l/Linc

# Añadimos cordones inferiores
ss.add_element(location=[[0,0], [0,4]], spring={2: 0})
ss.add_element(location=[[0,4], [3,4]])
ss.add_element(location=[[3,4], [4,2]])

# BCs
ss.add_support_hinged(node_id=1)
ss.add_support_hinged(node_id=4)

# Añadimos carga puntual al nodo 2
ss.q_load(element_id=1, q=(2,2))
ss.q_load(element_id=2, q=(0,10))
ss.q_load(element_id=3, q=ptot*cosa,q_perp=-ptot*sina)

# Mostramos estructura generada
ss.show_structure(title='Problema 2 extraordinaria ')

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
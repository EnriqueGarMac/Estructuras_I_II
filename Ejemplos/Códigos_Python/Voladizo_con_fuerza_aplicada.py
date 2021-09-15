# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""

from anastruct import SystemElements

ss = SystemElements()

L = 3.0  # Longitud de la barra
P = -100.0 # Carga puntual

# Añadimos elemento barra 1
ss.add_element(location=[[0, 0], [L, 0]])


# Añadimos empotramiento al nodo 1
ss.add_support_fixed(node_id=1)


# Añadimos carga puntual al nodo 2
ss.point_load(2, Fx=0, Fy=-P)

# Mostramos estructura generada
ss.show_structure(title='Viga simplemente apoyada')

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
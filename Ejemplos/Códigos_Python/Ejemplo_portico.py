# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements

ss = SystemElements()

L = 3.0  # Ancho
h = 4.0 # Alto
F = 100.0 # Carga puntual

# Añadimos elemento barra 1
ss.add_element(location=[[0, 0], [0,h]])
# Añadimos elemento barra 2
ss.add_element(location=[[0, h], [L,h]])
# Añadimos elemento barra 3
ss.add_element(location=[[L, h], [L,0]])


# Añadimos rótula al nodo 1
ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 4
ss.add_support_roll(node_id=4, direction=2)

# Añadimos carga puntual al nodo 2
ss.point_load(2, Fx=F, Fy=0)

# Mostramos estructura generada
# ss.show_structure(title='Viga simplemente apoyada')

# Resolvemos la estructura
ss.solve()

# Mostramos las reacciones
#ss.show_reaction_force()

# Mostramos cortantes
#ss.show_shear_force()

# Mostramos flectores
ss.show_bending_moment()

# Mostramos axiles
#ss.show_axial_force()

# Mostramos deformada
#ss.show_displacement()

# Mostramos todos los resultados juntos
#ss.plotter.results_plot()

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""

from anastruct import SystemElements

ss = SystemElements()

# Construcción de la estructura

# Viga 1
ss.add_element(location=[[0, 0], [1, 0]])
# Viga 2
ss.add_element(location=[[1, 0], [2, 0]])
# Viga 3
ss.add_element(location=[[2, 0], [3, 0]], spring={2: 0})
# Viga 4
ss.add_element(location=[[3, 0], [5, 0]])


# Condiciones de contorno

# Añadimos apoyo fijo al nodo 1
ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 3
ss.add_support_roll(node_id=3, direction=2)
# Añadimos carrito al nodo 5
ss.add_support_roll(node_id=5, direction=2)

# Cargas

# Añadimos carga puntual al nodo 2
ss.point_load(2, Fx=0, Fy=-10)

# Añadimos carga distribuida
ss.q_load(element_id=3, q=5)

# Añadimos carga distribuida
ss.q_load(element_id=4, q=5)

# Mostramos estructura generada
ss.show_structure(title='Práctica 1')

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
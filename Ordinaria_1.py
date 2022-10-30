# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements

ss = SystemElements()


Ey = 2.1*10**8 # Módulo de Young
Ar = 10*10**(-4) 

# Añadimos cordones inferiores
ss.add_truss_element(location=[[0,0], [1,0]],EA=Ey*4)
ss.add_truss_element(location=[[1,0], [4,0]],EA=Ey*4)
ss.add_truss_element(location=[[4,0], [6,0]],EA=Ey*2)


# Añadimos rótula al nodo 1
ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 4
ss.add_support_hinged(node_id=4)

# Añadimos carga puntual al nodo 2
ss.point_load(2, Fx=10)
ss.q_load(element_id=1, q=(0,0), q_perp=(0,1))
ss.q_load(element_id=2, q=(0,0), q_perp=(1,4))

# Mostramos estructura generada
ss.show_structure(title='Problema 1 ordinaria ')

# Resolvemos la estructura
ss.solve()

# Mostramos las reacciones
ss.show_reaction_force()


# Mostramos axiles
ss.show_axial_force()

# Mostramos deformada
ss.show_displacement(factor=1400)

# Mostramos todos los resultados juntos
#ss.plotter.results_plot()

ss.printdispl()
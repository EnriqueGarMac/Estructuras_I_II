# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements

ss = SystemElements()


Ey = 1 # Módulo de Young

# Añadimos cordones inferiores
ss.add_truss_element(location=[[0,0], [3,0]],EA=Ey*0.1)
ss.add_truss_element(location=[[3,0], [6,3]],EA=Ey*0.3)
ss.add_truss_element(location=[[0,0], [0,3]],EA=Ey*0.1)
ss.add_truss_element(location=[[0,3], [3,3]],EA=Ey*0.2)
ss.add_truss_element(location=[[3,3], [6,3]],EA=Ey*0.2)
ss.add_truss_element(location=[[3,0], [3,3]],EA=Ey*0.5)
ss.add_truss_element(location=[[0,0], [3,3]],EA=Ey*0.5)

# Añadimos rótula al nodo 1
ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 4
ss.add_support_roll(node_id=3, direction=2)

# Añadimos carga puntual al nodo 2
ss.point_load(4, Fy=-10)
ss.point_load(5, Fy=-10)


# Mostramos estructura generada
#ss.show_structure(title='Viga simplemente apoyada')

# Resolvemos la estructura
ss.solve()

# Mostramos las reacciones
#ss.show_reaction_force()

# Mostramos cortantes
#ss.show_shear_force()

# Mostramos flectores
# ss.show_bending_moment()

# Mostramos axiles
ss.show_axial_force()

# Mostramos deformada
ss.show_displacement()

# Mostramos todos los resultados juntos
#ss.plotter.results_plot()

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
ss.add_truss_element(location=[[0,0], [0,4]],EA=Ey*Ar)
ss.add_truss_element(location=[[0,4], [0,8]],EA=Ey*Ar)
ss.add_truss_element(location=[[0,4], [5,4]],EA=Ey*Ar)
ss.add_truss_element(location=[[0,0], [5,4]],EA=Ey*Ar)
ss.add_truss_element(location=[[5,0], [5,4]],EA=Ey*Ar)
ss.add_truss_element(location=[[5,4], [0,8]],EA=Ey*Ar)


# Añadimos rótula al nodo 1
ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 4
ss.add_support_hinged(node_id=5)

# Añadimos carga puntual al nodo 2
ss.point_load(2, Fx=10)
ss.point_load(3, Fy=-10, Fx=6)
ss.point_load(2, Fx=+12)
ss.point_load(1, Fx=+6)
ss.point_load(4, Fy=-10, Fx=-10)

# Mostramos estructura generada
ss.show_structure(title='Problema 2 ordinaria PTV_Castigliano')

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
ss.show_displacement(factor=1400)

# Mostramos todos los resultados juntos
#ss.plotter.results_plot()

ss.printdispl()
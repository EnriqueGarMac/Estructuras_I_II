# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements

ss = SystemElements()



# Añadimos cordones inferiores
ss.add_truss_element(location=[[0,0], [4,0]],EA=2.1*10**11*0.00006)
ss.add_truss_element(location=[[4,0], [8,0]],EA=2.1*10**11*0.00006)
ss.add_truss_element(location=[[0,0], [2,2]],EA=2.1*10**11*0.00006)
ss.add_truss_element(location=[[2,2], [6,2]],EA=2.1*10**11*0.00006)
ss.add_truss_element(location=[[6,2], [8,0]],EA=2.1*10**11*0.00006)
ss.add_truss_element(location=[[2,2], [4,0]],EA=2.1*10**11*0.00006)
ss.add_truss_element(location=[[4,0], [6,2]],EA=2.1*10**11*0.00006)


# Añadimos rótula al nodo 1
ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 4
ss.add_support_roll(node_id=3, direction=2)

# Añadimos carga puntual al nodo 2
ss.point_load(2, Fy=-10000)
ss.point_load(4, Fy=-1000)
ss.point_load(5, Fy=-1000)

# Mostramos estructura generada
ss.show_structure(title='Ejemplo Menabrea')

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
#ss.show_displacement()

# Mostramos todos los resultados juntos
#ss.plotter.results_plot()

ss.printdispl()
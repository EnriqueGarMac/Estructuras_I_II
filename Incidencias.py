# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements

ss = SystemElements()


Ey = 2.1*10**11 # Módulo de Young
Ar = 10*10**(-4) 

# Añadimos cordones inferiores
ss.add_truss_element(location=[[0,0], [2,4]],EA=Ey*Ar)
ss.add_truss_element(location=[[0,0], [4,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[2,4], [4,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[2,4], [6,4]],EA=Ey*Ar)
ss.add_truss_element(location=[[4,0], [6,4]],EA=Ey*Ar)
ss.add_truss_element(location=[[4,0], [6,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[6,0], [6,4]],EA=Ey*Ar)

# Condiciones de contorno
ss.add_support_roll(node_id=4, direction=1)
ss.add_support_hinged(node_id=5)

# Añadimos carga puntual al nodo 2
ss.point_load(3, Fy=10000)
ss.point_load(1, Fy=-2000, Fx=4000)
ss.point_load(2, Fy=-2000, Fx=4000)


# Mostramos estructura generada
ss.show_structure(title='Examen incidencias')

# Resolvemos la estructura
ss.solve()

# Mostramos las reacciones
#ss.show_reaction_force()

# Mostramos cortantes
#ss.show_shear_force()

# Mostramos flectores
# ss.show_bending_moment()

# Mostramos axiles
# ss.show_axial_force()

# Mostramos deformada
ss.show_displacement(factor=1400)

# Mostramos todos los resultados juntos
#ss.plotter.results_plot()

ss.printdispl()
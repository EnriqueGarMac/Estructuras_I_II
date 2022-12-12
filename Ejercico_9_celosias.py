# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 20:42:05 2022

@author: Enrique GM
"""

import numpy as np
from anastruct import SystemElements

ss = SystemElements()

Ar = 0.01 # Area
Ey = 210e+3 # Módulo de Young

# Añadimos cordones
ss.add_truss_element(location=[[0,0], [1,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[1.,0.], [2.,0.]],EA=Ey*Ar)
ss.add_truss_element(location=[[0.,0.], [1.0,-1]],EA=Ey*Ar)
ss.add_truss_element(location=[[1.0,-1], [2.0,-1]],EA=Ey*Ar)
ss.add_truss_element(location=[[2.0,-1], [3.0,-1.]],EA=Ey*Ar)
ss.add_truss_element(location=[[1.0,0.0], [1.,-1.]],EA=Ey*Ar)
ss.add_truss_element(location=[[2.,0.], [2.0,-1]],EA=Ey*Ar)
ss.add_truss_element(location=[[1.,0.], [2.0,-1]],EA=Ey*Ar)
ss.add_truss_element(location=[[2.,0.], [3.0,-1]],EA=Ey*Ar)

# Añadimos apoyo fijo al nudo 6
ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 9
ss.add_support_roll(node_id=6, direction=2)


# Añadimos carga puntual al nodo 2
ss.point_load(4, Fy=-3.)
ss.point_load(5, Fy=-6)

# Mostramos estructura generada
ss.show_structure(title='Ejercicio 3')

# Resolvemos la estructura
ss.solve();

# Mostramos las reacciones
ss.show_reaction_force()

# Mostramos axiles
ss.show_axial_force(printvalues=1,factor=0.1)


# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 20:42:05 2022

@author: Enrique GM
"""

import numpy as np
from anastruct import SystemElements

ss = SystemElements()

h = 2.0 # Ancho celda
hv = 1.0 # Alto celda

Ar = 0.01 # Area
Ey = 210e+3 # Módulo de Young

# Añadimos cordones
ss.add_truss_element(location=[[h/2,hv], [h/2+h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2+h,hv], [h/2+2*h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2+2*h,hv], [h/2+3*h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2+3*h,hv], [h/2+4*h,hv]],EA=Ey*Ar)

ss.add_truss_element(location=[[0,0], [h,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[h,0], [2*h,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[2*h,0], [3*h,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[3*h,0], [4*h,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[4*h,0], [5*h,0]],EA=Ey*Ar)

# Añadimos diagonales
ss.add_truss_element(location=[[0,0], [h/2.0,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0,hv], [h,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[h,0], [h+h/2.0,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h+h/2.0,hv], [2*h,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[2*h,0], [2*h+h/2.0,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[2*h+h/2.0,hv], [3*h,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[3*h,0], [3*h+h/2.0,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[3*h+h/2.0,hv], [4*h,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[4*h,0], [4*h+h/2.0,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[4*h+h/2.0,hv], [5*h,0]],EA=Ey*Ar)

# Añadimos apoyo fijo al nudo 6
ss.add_support_hinged(node_id=6)
# Añadimos carrito al nodo 9
ss.add_support_roll(node_id=9, direction=2)


# Añadimos carga puntual al nodo 2
ss.point_load(7, Fy=-1.0)
ss.point_load(8, Fy=-1.0)
ss.point_load(10, Fy=-0.5)
ss.point_load(11, Fy=-0.5)

# Mostramos estructura generada
ss.show_structure(title='Ejercicio 3')

# Resolvemos la estructura
ss.solve();

# Mostramos las reacciones
ss.show_reaction_force()

# Mostramos axiles
ss.show_axial_force(printvalues=1,factor=0.1)


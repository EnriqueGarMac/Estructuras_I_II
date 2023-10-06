# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements
import collections
collections.Iterable = collections.abc.Iterable

ss = SystemElements()

h = 3.0 # Ancho celda
hv = 2.6 # Alto montantes

Ar = 30*10**(-4) # Area barras
Aro = 30*10**(-4) # Area cordon inferior
Ey = 2.10e+11 # Módulo de Young

F1 = -(10*139*3/2)*h/2.0 # Carga F1


# Añadimos cordones inferiores
ss.add_truss_element(location=[[0,0], [h,0]],EA=Ey*Aro)
ss.add_truss_element(location=[[h,0], [2*h,0]],EA=Ey*Aro)
ss.add_truss_element(location=[[2*h,0], [3*h,0]],EA=Ey*Aro)
ss.add_truss_element(location=[[3*h,0], [4*h,0]],EA=Ey*Aro)
ss.add_truss_element(location=[[4*h,0], [5*h,0]],EA=Ey*Aro)
ss.add_truss_element(location=[[5*h,0], [6*h,0]],EA=Ey*Aro)

# Añadimos cordones superiores
ss.add_truss_element(location=[[h/2.0,hv], [h/2.0+h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0+h,hv], [h/2.0+2*h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0+2*h,hv], [h/2.0+3*h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0+3*h,hv], [h/2.0+4*h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0+4*h,hv], [h/2.0+5*h,hv]],EA=Ey*Ar)


# Añadimos diagonales
ss.add_truss_element(location=[[0,0], [h/2.0,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0,hv], [h,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[h,0], [h/2.0+h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0+h,hv], [2*h,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[2*h,0,0], [h/2.0+2*h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0+2*h,hv], [3*h,0,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[3*h,0,0], [h/2.0+3*h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0+3*h,hv], [4*h,0,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[4*h,0,0], [h/2.0+4*h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0+4*h,hv], [5*h,0,0]],EA=Ey*Ar)
ss.add_truss_element(location=[[5*h,0,0], [h/2.0+5*h,hv]],EA=Ey*Ar)
ss.add_truss_element(location=[[h/2.0+5*h,hv], [6*h,0,0]],EA=Ey*Ar)

# Añadimos rótula al nodo 1
ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 4
ss.add_support_roll(node_id=7, direction=2)

# Añadimos cargsa puntuales al nodo 2
ss.point_load(1, Fy=F1)
ss.point_load(2, Fy=2*F1)
ss.point_load(3, Fy=2*F1)
ss.point_load(4, Fy=2*F1)
ss.point_load(5, Fy=2*F1)
ss.point_load(6, Fy=2*F1)
ss.point_load(7, Fy=F1)

# Mostramos estructura generada
ss.show_structure(title='Viga simplemente apoyada')

# Resolvemos la estructura
ss.solve()

# Mostramos las reacciones
#ss.show_reaction_force()

# Mostramos cortantes
#ss.show_shear_force()

# Mostramos flectores
# ss.show_bending_moment()

# Mostramos axiles
#ss.show_axial_force()

# Mostramos deformada
#ss.show_displacement(factor=2000)

ss.printdispl()

# Mostramos todos los resultados juntos
#ss.plotter.results_plot()

# Limite
18./1200.
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""

from anastruct import SystemElements
ss = SystemElements()

L = 3.0  # Longitud de la barra
P = -10.0 # Carga puntual

# Añadimos elemento barra 1
ss.add_element(location=[[0, 0], [L/2.0, 0]])
# Añadimos elemento barra 2
ss.add_element(location=[[L/2.0, 0], [L, 0]])

# Añadimos apoyo fijo al nodo 1
ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 3
ss.add_support_roll(node_id=3, direction=2)

# Añadimos carga puntual al nodo 2
ss.point_load(2, Fx=P, rotation=-90)

# Mostramos estructura generada
ss.show_structure()

# Mostramos cortantes
ss.show_shear_force()
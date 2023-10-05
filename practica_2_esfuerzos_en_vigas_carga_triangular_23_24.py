# -*- coding: utf-8 -*-
"""Practica_2_Esfuerzos_en_vigas_carga_triangular_23_24.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bBSl5MHVqSZYUEHMP1q-JKfuuTxm3iEI
"""

# Instalar paquete anastruct
#!pip install git+https://github.com/EnriqueGarMac/Estructuras_I_II.git

import numpy as np
from anastruct import SystemElements
import collections
collections.Iterable = collections.abc.Iterable


ss = SystemElements()

L1 = 2.0  # m
L2 = 6.0 # m
q = 15 # Carga triangular kN/m
P = 40 # Carga puntual kN
Mp = 20 # Momento puntual kNm


# Añadimos elemento barra 1
ss.add_element(location=[[0, 0], [L1,0]])
# Añadimos elemento barra 2
ss.add_element(location=[[L1, 0], [L1+L2,0]])

# Añadimos carrito al nodo 2
ss.add_support_roll(node_id=2, direction=2)

# Añadimos apoyo fijo al nodo 3
ss.add_support_hinged(node_id=3)

# Añadimos carga puntual al nodo 1
ss.point_load(1, Fx=0, Fy=-P)

# Añadimos momento puntual al nodo 1
ss.moment_load(1, Ty=Mp)

# Añadimos carga triangular
ss.q_load(element_id=1, q=(0,L1*q/(L1+L2)), q_perp=(0,0))
ss.q_load(element_id=2, q=(L1*q/(L1+L2),q), q_perp=(0,0))

# Mostramos estructura generada
ss.show_structure(title='Ejercicio 2 práctica esfuerzos en vigas 2023_2024')

# Resolvemos la estructura
ss.solve()

# Mostramos las reacciones
ss.show_reaction_force()

# Mostramos cortantes
ss.show_shear_force()

# Mostramos flectores
ss.show_bending_moment()

ss.show_displacement()
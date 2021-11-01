# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements


# Cargamos el objeto para las viguetas
ss = SystemElements()

# Vamos a definir ahora algunas variables
L = 5.0  # Longitud de las viguetas [m]
s = 0.6 # Distancia inter-eje [s]
Q = 0.9*1.5+(0.18+3.0)*1.35  # Carga por unidad de superficie [kN/m2]
qv = Q*s  # Carga por unidad de longitud de vigueta

# Construcción de la estructura
# Añadimos elemento barra 1
ss.add_element(location=[[0, 0], [L, 0]]);

# Añadimos apoyo fijo al nodo 1
ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 3
ss.add_support_roll(node_id=2, direction=2)

# Añadimos carga uniformemente distribuida
ss.q_load(element_id=1, q=qv)

# Resolvemos la estructura
ss.solve();

# Mostramos flectores
ss.show_bending_moment()

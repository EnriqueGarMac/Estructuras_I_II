# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements

# Cargamos el objeto para el pórtico
sp = SystemElements()

# Vamos a definir ahora algunas variables
h = 3.0  # Altura del pórtico
w = 3.5 # Ancho del pórtico
dp = 5 # Longitud de la cubierta
qv1 = 2.3*1.5   # Carga de viento soporte izquierdo
qv2 = 1.2*1.5   # Carga de viento soporte derecho
Q = 0.9*1.5+(0.18+3.0)*1.35  # Carga por unidad de superficie en cubierta [kN/m2]
qf1 = -Q*dp/2.0+3*1.5  # Carga en viga por izquierda [kN/m2]
qf2 = -Q*dp/2.0+2*1.5  # Carga en viga por derecha [kN/m2]

# Añadimos soporte 1 AB
sp.add_element(location=[[0, 0], [0, h]]);
# Añadimos viga BC(izquierda)
sp.add_element(location=[[0, h], [w/2.0, h]]);
# Añadimos viga BC (izquierda)
sp.add_element(location=[[w/2.0, h], [w, h]]);
# Añadimos soporte 2 CD
sp.add_element(location=[[w, h], [w, 0]]);

# Añadimos apoyo fijo al nodo 1
sp.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 3
sp.add_support_roll(node_id=5, direction=2)

# Añadimos carga uniformemente distribuida
sp.q_load(element_id=1, q=qv1)
# Añadimos carga uniformemente distribuida
sp.q_load(element_id=2, q=-qf1)
# Añadimos carga uniformemente distribuida
sp.q_load(element_id=3, q=-qf2)
# Añadimos carga uniformemente distribuida
sp.q_load(element_id=4, q=-qv2)

# Mostramos estructura generada
sp.show_structure(title='Pórtico')

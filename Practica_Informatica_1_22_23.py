# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements


# Cargamos el objeto de nuestra estructura
ss = SystemElements()

# Construcción de la estructura

# Añadimos elemento barra 1
ss.add_element(location=[[1, 0], [1, 1.5]]);
# Añadimos elemento barra 2
ss.add_element(location=[[1, 1.5], [1, 4.5]]);
# Añadimos elemento barra 3
ss.add_element(location=[[0, 4.5], [1, 4.5]]);
# Añadimos elemento barra 4
ss.add_element(location=[[1, 4.5], [4, 4.5]], spring={2: 0});
# Añadimos elemento barra 5
ss.add_element(location=[[4, 4.5], [7, 4.5]]);
# Añadimos elemento barra 6
ss.add_element(location=[[7, 4.5], [7, 3.5]]);
# Añadimos elemento barra 7
ss.add_element(location=[[7, 3.5], [7, 0.0]]);
# Añadimos elemento barra 8
ss.add_element(location=[[7, 3.5], [8, 3.5]]);


# Añadimos apoyo fijo al nodo 1
ss.add_support_fixed(node_id=1)
# Añadimos carrito al nodo 3
ss.add_support_roll(node_id=8, direction=2)

# Añadimos carga puntual
ss.point_load(4, Fx=0.0, Fy=-10.0)
# Añadimos cargas distribuidas
ss.q_load(element_id=1, q=(0,4), q_perp=(0,0))
ss.q_load(element_id=2, q=(4,4), q_perp=(0,0))
ss.q_load(element_id=5, q=(2,2), q_perp=(0,0))
# Añadimos momento puntual
ss.moment_load(9, Ty=-5)

# Resolvemos la estructura
ss.solve();

# Mostramos las reacciones
ss.show_reaction_force()


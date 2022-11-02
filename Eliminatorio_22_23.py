# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 21:19:59 2022

@author: Enrique GM
"""

from anastruct import SystemElements

ss = SystemElements(mesh=18000)


# Añadimos elemento barra 1
ss.add_element(location=[[0, 0], [3.0, 0]], spring={2: 0})
# Añadimos elemento barra 2
ss.add_element(location=[[3.0, 0], [4.0, 0]])
# Añadimos elemento barra 3
ss.add_element(location=[[4.0, 0], [5.0, 0]])
# Añadimos elemento barra 4
ss.add_element(location=[[5.0, 0], [6.0, 0]])

# Añadimos apoyo fijo al nodo 1
ss.add_support_fixed(node_id=5)
# Añadimos carrito al nodo 3
ss.add_support_roll(node_id=1, direction=2)

# Cargas
ss.q_load(element_id=1, q=(2,4))
ss.moment_load(4, Ty=10)
ss.point_load(3, Fx=0, Fy=-10)

# Mostramos estructura generada
ss.show_structure(title='Eliminatorio 22/23')

# Resolvemos la estructura
ss.solve()

# Mostramos flectores
ss.show_bending_moment()
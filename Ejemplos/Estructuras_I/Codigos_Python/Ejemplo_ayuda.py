# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 18:31:58 2021

@author: Enrique GM
"""
from anastruct import SystemElements
import collections
collections.Iterable = collections.abc.Iterable

# Crear objeto para la estructura
ss = SystemElements()

ss.add_element(location=[[0, 0], [3, 4]])
ss.add_element(location=[[3, 4], [8, 4]])

ss.add_support_hinged(node_id=1)
ss.add_support_fixed(node_id=3)

ss.q_load(element_id=2, q=-10)
ss.solve()

ss.show_structure()

ss.show_reaction_force()


ss.show_axial_force()


ss.show_shear_force()


ss.show_bending_moment()


ss.show_displacement()

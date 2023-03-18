# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 13:54:16 2021

@author: Enrique GM
"""
import numpy as np
from anastruct import SystemElements

ss = SystemElements()


#Ey = 210000 # Módulo de Young N/mm2 Acero
Ey = 70000 # Módulo de Young N/mm2 Aluminio
sx  = 500  # mm
sy = 288.675  # mm

# 40.2
Area = 2.90*10**2
IY = 6.60*10**4

# https://www.leroymerlin.es/fp/80109694/perfil-forma-tubo-cuadrado-de-aluminiox2-4x100-cm0-15
base = 10.
es = 1.
A = base*base-(base-2.*es)*(base-2.*es)
IY = (1./12.)*base**4-(1./12.)*(base-2.*es)**4.
   
Lmax = np.sqrt(sx**2+sy**2)
Pcr = 0.8*np.pi**2*Ey*IY/Lmax**2

EAbarra = Ey*Area

# Añadimos cordones inferiores
ss.add_truss_element(location=[[0,0], [sx,0]],EA=EAbarra)
ss.add_truss_element(location=[[sx,0], [2*sx,0]],EA=EAbarra)
ss.add_truss_element(location=[[2*sx,0], [3*sx,0]],EA=EAbarra)
ss.add_truss_element(location=[[sx,0], [sx,sy]],EA=EAbarra)
ss.add_truss_element(location=[[2*sx,0], [2*sx,sy]],EA=EAbarra)
ss.add_truss_element(location=[[0,sy], [sx,sy]],EA=EAbarra)
ss.add_truss_element(location=[[sx,sy], [2*sx,sy]],EA=EAbarra)

kr = 11.07
Lo = 139.70
Lb = (Lmax-Lo)
Keqm = 1./(Lb/(EAbarra)+1/kr)
Keq = EAbarra*Lmax

ss.add_truss_element(location=[[0,sy], [sx,0]],EA=Keq*Lmax)
ss.add_truss_element(location=[[sx,sy], [2*sx,0]],EA=Keq*Lmax)
ss.add_truss_element(location=[[2*sx,sy], [3*sx,0]],EA=Keq*Lmax)


# Añadimos rótula al nodo 1
ss.add_support_roll(node_id=1, direction=1)
#ss.add_support_hinged(node_id=1)
# Añadimos carrito al nodo 4
ss.add_support_hinged(node_id=7)


# Añadimos carga puntual al nodo 2
ss.point_load(4, Fy=-9.81*1000/1000)


# Mostramos estructura generada
ss.show_structure()

# Resolvemos la estructura
ss.solve()

# Mostramos las reacciones
#ss.show_reaction_force()

# Mostramos cortantes
#ss.show_shear_force()

# Mostramos flectores
# ss.show_bending_moment()

# Mostramos axiles
ss.show_axial_force()

# Mostramos deformada
ss.show_displacement(factor = 1)

# Mostramos todos los resultados juntos
# ss.plotter.results_plot()
ss.printdispl()
# ss.get_node_displacements(0)
import sys
from setuptools import setup
import collections
collections.Iterable = collections.abc.Iterable

setup(
    name="anastruct",
    description="Análisis de pórticos planos",
    author="Enrique GM",
    author_email="enriquegm@ugr.es",
    url="https://github.com/EnriqueGarMac/Estructuras_I_II",
    license="GPL-3.0",
    packages=[
        "anastruct",
        "anastruct.fem",
        "anastruct.fem.system_components",
        "anastruct.fem.examples",
        "anastruct.material",
        "anastruct.cython",
        "anastruct.fem.cython",
        "anastruct.fem.plotter",
        "anastruct.fem.util",
        "anastruct.sectionbase",
    ],
    install_requires=["matplotlib>=3.0", "numpy>=1.15.4", "scipy>=1.1.0"],
)

# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 13:32:45 2022

# Toolboxes
!pip install pdfgen
!pip install notebook-as-pdf
!pyppeteer-install
!pip install pdfkit
!apt-get install texlive texlive-xetex texlive-latex-extra pandoc
!pip install pypandoc
!pip install PyPDF2
@author: Enrique GM
"""


import pdfkit
from PyPDF2 import PdfMerger
import os


#Define path to wkhtmltopdf.exe
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

#Point pdfkit configuration to wkhtmltopdf.exe
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)


documents = ['Tutorial_basico_Python.ipynb']


cont = 1
for i in documents:
 name_file = i
 name_output = 'output_'+str(cont)+'.html'
 name_output_pdf = 'output_'+str(cont)+'.pdf'
 !jupyter nbconvert --to pdf $name_file --EmbedImagesPreprocessor.embed_images=True --output=$name_output
 cont += 1
 #pdfkit.from_file(name_output, name_output_pdf, configuration=config)
 #merger.append(name_output_pdf, import_bookmarks=False)
 #os.remove(name_output)
 #os.remove(name_output_pdf)

cont = 1
merger = PdfMerger()
for i in documents:
 name_file = i
 name_output = 'output_'+str(cont)+'.html'
 name_output_pdf = 'output_'+str(cont)+'.pdf'
 cont += 1
 pdfkit.from_file(name_output, name_output_pdf, configuration=config)
 merger.append(name_output_pdf, import_bookmarks=False)
 #os.remove(name_output)
 #os.remove(name_output_pdf)

merger.write("Apuntes_completos.pdf")
merger.close()
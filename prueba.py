from dataclasses import dataclass, field
from typing import Optional
import requests 
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
} #Requiero esto para que wikipedia no me corte el acceso a su API

tablas = pd.read_html("https://es.wikipedia.org/wiki/Copa_Mundial_de_F%C3%BAtbol",
                      storage_options={"User-Agent": headers["User-Agent"]})
tablasPartido = pd.read_html("https://es.wikipedia.org/wiki/Anexo:Calendario_de_la_Copa_Mundial_de_F%C3%BAtbol_de_2026#Partidos",
                      storage_options={"User-Agent": headers["User-Agent"]})
tablaPartido = tablasPartido[2]
partidos = tablaPartido[["Equipo 1", "Equipo 2"]].dropna(subset=["Equipo 1", "Equipo 2"])
# Ver todos los nombres únicos de selecciones
df = pd.read_csv("results.csv")

# Equipos que aparecen en el fixture del 2026
equipos_2026 = pd.unique(partidos[["Equipo 1", "Equipo 2"]].values.ravel())
print(sorted(equipos_2026))
from dataclasses import dataclass, field
from typing import Optional
import requests 
from bs4 import BeautifulSoup
import pandas as pd


@dataclass
class Seleccion:
    nombre: str
    puntaje: int=0
    mundiales_jugados: list[int] = field(default_factory=list)

    def agregar_resultado(self,anio: int,puntos: int) -> None:
        self.mundiales_jugados.append(anio)
        self.puntaje += puntos

ALIASES = {
    "Alemania Federal":"Alemania",
    "Union Sovietica": "Rusia",
    "Checoslovaquia": "República Checa",
    "Yugoslavia": "Serbia",
}
TRADUCCION = {
    "Germany": "Alemania",
    "Saudi Arabia": "Arabia Saudita",
    "Algeria": "Argelia",
    "Argentina": "Argentina",
    "Australia": "Australia",
    "Austria": "Austria",
    "Bosnia and Herzegovina": "Bosnia y Herzegovina",
    "Brazil": "Brasil",
    "Belgium": "Bélgica",
    "Cape Verde": "Cabo Verde",
    "Canada": "Canadá",
    "Qatar": "Catar",
    "Colombia": "Colombia",
    "South Korea": "Corea del Sur",
    "Ivory Coast": "Costa de Marfil",
    "Croatia": "Croacia",
    "Curaçao": "Curazao",
    "Ecuador": "Ecuador",
    "Egypt": "Egipto",
    "Scotland": "Escocia",
    "Spain": "España",
    "United States": "Estados Unidos",
    "France": "Francia",
    "Ghana": "Ghana",
    "Haiti": "Haití",
    "England": "Inglaterra",
    "Iraq": "Irak",
    "Iran": "Irán",
    "Japan": "Japón",
    "Jordan": "Jordania",
    "Morocco": "Marruecos",
    "Mexico": "México",
    "Norway": "Noruega",
    "New Zealand": "Nueva Zelanda",
    "Panama": "Panamá",
    "Paraguay": "Paraguay",
    "Netherlands": "Países Bajos",
    "Portugal": "Portugal",
    "Czech Republic": "República Checa",
    "DR Congo": "República Democrática del Congo",
    "Senegal": "Senegal",
    "South Africa": "Sudáfrica",
    "Sweden": "Suecia",
    "Switzerland": "Suiza",
    "Turkey": "Turquía",
    "Tunisia": "Túnez",
    "Uruguay": "Uruguay",
    "Uzbekistan": "Uzbekistán",
}
PUNTAJES = {
    "Campeón": 10,
    "Subcampeón": 6,
    "Tercer lugar": 4,
    "Cuarto lugar":2,
}
def normalizar(nombre:str) -> str:
    return ALIASES.get(nombre,nombre)

def cargar_datos(tabla: pd.DataFrame) -> dict[str,Seleccion]:
    selecciones: dict[str,Seleccion] = {}

    for _,fila in tabla.iterrows():
        if "No celebrada" in str(fila["Campeón"]):
            continue
        if "Por disputarse" in str(fila["Campeón"]):
            continue

        anio = int(str(fila["Edición"]).replace("Detalles","").strip())

        for columna, puntos in PUNTAJES.items():
            nombre = normalizar(str(fila[columna]).strip())
            if nombre not in selecciones:
                selecciones[nombre] = Seleccion(nombre=nombre)
        
            selecciones[nombre].agregar_resultado(anio, puntos)

    return selecciones

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
} #Requiero esto para que wikipedia no me corte el acceso a su API

tablas = pd.read_html("https://es.wikipedia.org/wiki/Copa_Mundial_de_F%C3%BAtbol",
                      storage_options={"User-Agent": headers["User-Agent"]})
tablasPartido = pd.read_html("https://es.wikipedia.org/wiki/Anexo:Calendario_de_la_Copa_Mundial_de_F%C3%BAtbol_de_2026#Partidos",
                      storage_options={"User-Agent": headers["User-Agent"]})

tabla_ediciones = tablas[2]
selecciones = cargar_datos(tabla_ediciones)

tablaPartido = tablasPartido[2]
partidos = tablaPartido[["Equipo 1", "Equipo 2"]].dropna(subset=["Equipo 1", "Equipo 2"])

#Mostrar resultado por puntaje
#for sel in sorted(selecciones.values(), key=lambda s:s.puntaje,reverse=True):
 #   print(f"{sel.nombre:<25} Puntaje:{sel.puntaje:>3} Mundiales: {sel.mundiales_jugados}")

for _, partido in partidos.iterrows():
    nombre1 = normalizar(partido["Equipo 1"].strip())
    nombre2 = normalizar(partido["Equipo 2"].strip())

    if nombre1 == "–" or nombre2 == "–":
        continue

        # Si no tienen historial, puntaje 0
    pts1 = selecciones[nombre1].puntaje if nombre1 in selecciones else 0
    pts2 = selecciones[nombre2].puntaje if nombre2 in selecciones else 0

    if pts1 > pts2:
        print(f"{nombre1} ({pts1} pts) gana a {nombre2} ({pts2} pts)")
    elif pts2 > pts1:
        print(f"{nombre2} ({pts2} pts) gana a {nombre1} ({pts1} pts)")
    else:
        print(f"Empate técnico: {nombre1} y {nombre2} ({pts1} pts)")



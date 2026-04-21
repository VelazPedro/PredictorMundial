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
#print(sorted(equipos_2026))


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


def traducir(nombre:str) -> str:
    return TRADUCCION.get(nombre,nombre)
def normalizar(nombre:str) -> str:
    return ALIASES.get(nombre,nombre)

df["date"] = pd.to_datetime(df["date"])
df_reciente = df[df["date"] >= "2022-12-18"] #Fecha ultimo mundial

df_reciente["home_team"] = df_reciente["home_team"].apply(traducir)
df_reciente["away_team"] = df_reciente["away_team"].apply(traducir)

@dataclass
class Seleccion:
    nombre: str
    puntaje: int=0

def cargar_datos_recientes(tabla: pd.DataFrame) -> dict[str,Seleccion]:
    selecciones: dict[str,Seleccion] = {}
    equipos = pd.unique(tabla[["home_team","away_team"]].values.ravel())
    for equipo in equipos:
        if equipo not in selecciones:
            selecciones[equipo] = Seleccion(nombre=equipo)
    return selecciones

selecciones = cargar_datos_recientes(df_reciente)

def calcular_puntaje_reciente(df: pd.DataFrame, selecciones: dict[str, Seleccion]) -> None:
    for _, fila in df.iterrows():
        if pd.isna(fila["home_score"]) or pd.isna(fila["away_score"]):
            continue
        local = fila["home_team"]
        visitante = fila["away_team"]
        diff = fila["home_score"] - fila["away_score"]

        if local in selecciones:
            selecciones[local].puntaje += diff * 1
        if visitante in selecciones:
            selecciones[visitante].puntaje -= diff * 1
calcular_puntaje_reciente(df_reciente,selecciones)
for sel in sorted(selecciones.values(), key=lambda s:s.puntaje,reverse=True):
    print(f"{sel.nombre:<25} Puntaje: {sel.puntaje:>8.2f}")

    

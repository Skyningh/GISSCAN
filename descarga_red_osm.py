# -*- coding: utf-8 -*-
"""Descarga la red vial drive de la Provincia de Santiago (OSM) y la guarda en parquet.

Se ejecuta una sola vez (los notebooks recargan el parquet). Guarda:
- datos/limite_provincia.geojson  — límite administrativo OSM (relación 1674530)
- datos/comunas.geojson           — comunas (admin_level=8) dentro de la provincia
- datos/red_drive_santiago.parquet — aristas dirigidas (GeoDataFrame EPSG:3857)
"""
import time
from pathlib import Path

import geopandas as gpd
import osmnx as ox

# ============================================================
# CONFIGURACIÓN DE LA CIUDAD Y ETIQUETA DE ARCHIVOS
# ============================================================

CONSULTA_CIUDAD = "provincia de santiago, Chile"   # Nombre para buscar en OSM
NOMBRE_CIUDAD = "santiago"           # Etiqueta para los archivos (DEBE coincidir con Paso 1 clasificación)

ox.settings.use_cache = True
ox.settings.log_console = True

BASE = Path(__file__).parent
DATOS = BASE / "00_descarga"
DATOS.mkdir(exist_ok=True)

t0 = time.time()

print(">>> límite provincial", flush=True)
prov = ox.geocode_to_gdf(CONSULTA_CIUDAD)
prov.to_file(DATOS / f"limite_{NOMBRE_CIUDAD}.geojson", driver="GeoJSON")       #Archivo creado
poligono = prov.geometry.iloc[0]

print(">>> comunas (admin_level=8)", flush=True)
try:
    comunas = ox.features_from_polygon(poligono, tags={"boundary": "administrative", "admin_level": "8"})
    comunas = comunas[comunas.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
    cols = [c for c in ["name"] if c in comunas.columns]
    comunas = comunas[cols + ["geometry"]].reset_index(drop=True)
    comunas.to_file(DATOS / f"comunas_{NOMBRE_CIUDAD}.geojson", driver="GeoJSON")       #Archivo creado
    print("comunas:", len(comunas), flush=True)
except Exception as e:
    print("comunas fallaron (no crítico):", e, flush=True)

print(">>> red vial drive de toda la provincia (esto tarda)", flush=True)
G = ox.graph_from_polygon(poligono, network_type="drive", retain_all=True, truncate_by_edge=True)
print("grafo:", len(G.nodes), "nodos,", len(G.edges), "aristas |", round(time.time() - t0), "s", flush=True)

edges = ox.graph_to_gdfs(G, nodes=False).reset_index()

def primero(v):
    return v[0] if isinstance(v, list) else v

edges["highway_osm"] = edges["highway"].apply(primero)
edges["nombre"] = edges["name"].apply(primero) if "name" in edges.columns else None
edges = edges[["u", "v", "key", "highway_osm", "nombre", "oneway", "geometry"]]
edges["nombre"] = edges["nombre"].astype(str)
edges = edges.to_crs(epsg=3857)

edges.to_parquet(DATOS / f"red_drive_{NOMBRE_CIUDAD}.parquet")              #Archivo creado 
print("guardado parquet:", len(edges), "aristas dirigidas |", round(time.time() - t0), "s total", flush=True)
print(f"LISTO_DESCARGA_{NOMBRE_CIUDAD}", flush=True)

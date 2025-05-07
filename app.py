
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import pandas as pd
import sqlite3
from datetime import datetime
from urllib.parse import urlparse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Cargar modelo
modelo = joblib.load("modelo_xgboost_urls.pkl")

# Conexión a base de datos
conn = sqlite3.connect("urls.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS historial_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    clasificacion TEXT,
    probabilidad REAL,
    fecha TEXT
)
""")
conn.commit()

def extraer_caracteristicas(url: str):
    parsed = urlparse(url)
    longitud = len(url)
    digitos = sum(c.isdigit() for c in url)
    guiones = url.count("-")
    https = 1 if parsed.scheme == "https" else 0
    puntos = url.count(".")
    subdominios = parsed.netloc.count(".")
    prefijo_guion = int("-" in parsed.netloc.split(".")[0])
    acortador = int(any(s in url for s in ["bit.ly", "t.co", "tinyurl"]))
    subdominio_raro = int(len(parsed.netloc.split(".")) > 3)
    tld_sospechoso = int(url.endswith((".tk", ".ml", ".ga", ".cf", ".gq")))
    return [
        longitud, digitos, guiones, https,
        puntos, subdominios, prefijo_guion,
        subdominio_raro, acortador, tld_sospechoso
    ]

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    cursor.execute("SELECT url, clasificacion, probabilidad, fecha FROM historial_urls ORDER BY id DESC LIMIT 10")
    historial = cursor.fetchall()
    cursor.execute("SELECT clasificacion, COUNT(*) FROM historial_urls GROUP BY clasificacion")
    resumen = cursor.fetchall()
    return templates.TemplateResponse("formulario.html", {
        "request": request,
        "historial": historial,
        "resumen": resumen
    })

@app.post("/", response_class=HTMLResponse)
async def analizar_url(request: Request, url: str = Form(...)):
    caracteristicas = extraer_caracteristicas(url)
    entrada = pd.DataFrame([caracteristicas], columns=[
        "longitud_url", "cantidad_digitos", "cantidad_guiones", "https",
        "nb_dots", "nb_subdomains", "prefix_suffix",
        "abnormal_subdomain", "shortening_service", "suspecious_tld"
    ])
    prob = modelo.predict_proba(entrada)[0][1]
    clasificacion = "maliciosa" if prob > 0.5 else "segura"

    explicacion = []
    if entrada["shortening_service"][0] == 1:
        explicacion.append("⚠️ La URL utiliza un acortador (bit.ly, tinyurl, etc.).")
    if entrada["suspecious_tld"][0] == 1:
        explicacion.append("⚠️ Dominio con extensión sospechosa (.tk, .ml, etc.).")
    if entrada["prefix_suffix"][0] == 1:
        explicacion.append("⚠️ El dominio tiene un guión, lo cual es inusual.")
    if entrada["abnormal_subdomain"][0] == 1:
        explicacion.append("⚠️ Uso de subdominios inusuales.")
    if entrada["https"][0] == 0:
        explicacion.append("⚠️ La URL no usa HTTPS.")
    if not explicacion:
        explicacion.append("✅ No se detectaron patrones sospechosos.")

    cursor.execute("INSERT INTO historial_urls (url, clasificacion, probabilidad, fecha) VALUES (?, ?, ?, ?)", (
        url, clasificacion, float(prob), datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()

    cursor.execute("SELECT url, clasificacion, probabilidad, fecha FROM historial_urls ORDER BY id DESC LIMIT 10")
    historial = cursor.fetchall()
    cursor.execute("SELECT clasificacion, COUNT(*) FROM historial_urls GROUP BY clasificacion")
    resumen = cursor.fetchall()

    return templates.TemplateResponse("formulario.html", {
        "request": request,
        "url": url,
        "probabilidad": round(prob * 100, 2),
        "clasificacion": clasificacion,
        "explicacion": explicacion,
        "historial": historial,
        "resumen": resumen
    })

# -url-phishing-detector
App web para detectar URLs maliciosas usando IA (XGBoost + FastAPI)

🛡️ URL Phishing Detector – App Web con Inteligencia Artificial
Este proyecto es una aplicación web desarrollada con FastAPI, Bootstrap y XGBoost que detecta URLs maliciosas usando modelos de machine learning.

🎯Objetivo
Ayudar a los usuarios a verificar si una URL es potencialmente peligrosa, mostrando:

La probabilidad de que sea maliciosa

Una breve explicación basada en características

Un historial con gráficas para análisis

🧠 ¿Cómo funciona?
Entrenamos un modelo de XGBoost con características como:

longitud de URL

cantidad de dígitos y guiones

uso de HTTPS

dominio sospechoso, subdominios, acortadores

El modelo predice y justifica por qué una URL puede ser riesgosa.

🌐 Tecnologías usadas
FastAPI (API web)

Jinja2 (plantillas HTML)

Chart.js (visualización de datos)

XGBoost, scikit-learn, pandas (modelo ML)

🚀 Despliegue en Render
Puedes desplegar esta app en https://render.com usando:

start.sh

Procfile

requirements.txt

📦 Instalación local

pip install -r requirements.txt
uvicorn app:app --reload
Luego abre: http://127.0.0.1:8000

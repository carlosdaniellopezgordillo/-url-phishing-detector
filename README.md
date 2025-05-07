# 🛡️ URL Phishing Detector – App Web con Inteligencia Artificial

Este proyecto es una aplicación web desarrollada con **FastAPI**, **Bootstrap** y **XGBoost** que detecta URLs maliciosas usando modelos de machine learning.

## 🎯 Objetivo
Ayudar a los usuarios a **verificar si una URL es potencialmente peligrosa**, mostrando:
- La probabilidad de que sea maliciosa
- Una breve explicación basada en características técnicas
- Un historial con gráficas para análisis

## 🧠 ¿Cómo funciona?
- Entrenamos un modelo XGBoost con características como:
  - longitud de URL
  - cantidad de dígitos y guiones
  - uso de HTTPS
  - subdominios sospechosos y acortadores
- La app clasifica la URL y explica las razones.

## 🌐 Tecnologías usadas
- `FastAPI` (API web)
- `Jinja2` (HTML dinámico)
- `Chart.js` (gráficos de resultados)
- `XGBoost`, `pandas`, `scikit-learn` (modelo IA)

## 🚀 Despliegue en Render
Puedes desplegar esta app gratis en [https://render.com](https://render.com) usando:
- `Procfile`
- `start.sh`
- `requirements.txt`

## 📦 Instalación local
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Luego abre tu navegador en:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📁 Archivos clave
- `app.py`: servidor FastAPI
- `formulario.html`: plantilla de resultados
- `modelo_xgboost_urls.pkl`: modelo entrenado (debes colocarlo tú)
- `urls.db`: base de datos de historial
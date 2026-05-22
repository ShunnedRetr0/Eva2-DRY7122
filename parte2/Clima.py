"""
========================================================
Evaluación N°2 - DRY7122
Parte 2: Consumo de API Pública (OpenWeatherMap)

Nota: Se utiliza OpenWeatherMap en reemplazo de MapQuest
debido a que esta última actualmente requiere ingresar 
datos de tarjeta de crédito para generar tokens API,
incluso para el plan gratuito (evidencia adjunta).

La API key se obtiene desde una variable de entorno
para no exponerla en el código fuente. Esta es una
buena práctica de seguridad: evita filtraciones cuando
el código se sube a repositorios públicos como GitHub.

Para ejecutar:
    export OPENWEATHER_API_KEY="tu_api_key_real"
    python3 clima.py

Autor: [Manuel Arrué y Jairo Soto]
Fecha: [21/05/2026]
========================================================
"""

import os
import sys
import json
import requests
from datetime import datetime

# ============================================
# CONFIGURACIÓN
# ============================================
# La API key se lee desde la variable de entorno OPENWEATHER_API_KEY
# Esto evita que la clave quede expuesta en el código fuente.
API_KEY = os.getenv("OPENWEATHER_API_KEY")
URL_BASE = "https://api.openweathermap.org/data/2.5/weather"


def consultar_clima(ciudad, pais="CL"):
    """
    Consulta el clima actual de una ciudad usando la API de OpenWeatherMap.
    
    Args:
        ciudad (str): Nombre de la ciudad a consultar
        pais (str): Código de país ISO 3166 (CL para Chile por defecto)
    
    Returns:
        requests.Response: Respuesta HTTP de la API
    """
    parametros = {
        "q": f"{ciudad},{pais}",
        "appid": API_KEY,
        "units": "metric",   # Temperatura en Celsius
        "lang": "es"          # Respuestas en español
    }
    
    print(f"\n🔗 URL de consulta: {URL_BASE}")
    print(f"📋 Parámetros: ciudad={ciudad}, país={pais}\n")
    
    respuesta = requests.get(URL_BASE, params=parametros)
    return respuesta


def mostrar_resultado(respuesta, ciudad):
    """
    Muestra el resultado de la consulta de forma legible.
    """
    print("=" * 60)
    print(f"  RESULTADO DE LA CONSULTA - HTTP {respuesta.status_code}")
    print("=" * 60)
    
    if respuesta.status_code != 200:
        print(f"❌ Error al consultar la API:")
        print(f"   Mensaje: {respuesta.text}")
        return
    
    datos = respuesta.json()
    
    print(f"\n📍 Ciudad:           {datos['name']}, {datos['sys']['country']}")
    print(f"🌡️  Temperatura:      {datos['main']['temp']}°C")
    print(f"🥵 Sensación térmica: {datos['main']['feels_like']}°C")
    print(f"💧 Humedad:          {datos['main']['humidity']}%")
    print(f"🌬️  Viento:           {datos['wind']['speed']} m/s")
    print(f"☁️  Condición:        {datos['weather'][0]['description'].capitalize()}")
    print(f"🔽 Presión:          {datos['main']['pressure']} hPa")
    print(f"👁️  Visibilidad:      {datos.get('visibility', 'N/A')} m")
    
    print(f"\n🗺️  Coordenadas:")
    print(f"   Latitud:  {datos['coord']['lat']}")
    print(f"   Longitud: {datos['coord']['lon']}")
    
    print("\n" + "=" * 60)
    print("📦 RESPUESTA JSON COMPLETA:")
    print("=" * 60)
    print(json.dumps(datos, indent=2, ensure_ascii=False))


def main():
    print("=" * 60)
    print("   CONSULTA DE CLIMA - API OpenWeatherMap")
    print("   Evaluación N°2 DRY7122")
    print(f"   Ejecutado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    # Validación: la API key debe estar configurada como variable de entorno
    if not API_KEY:
        print("\n⚠️  ERROR: La variable de entorno OPENWEATHER_API_KEY no está configurada.")
        print("\n    Para configurarla, ejecuta en la terminal ANTES del script:")
        print('        export OPENWEATHER_API_KEY="tu_api_key_real"')
        print("\n    Luego ejecuta:")
        print("        python3 clima.py\n")
        sys.exit(1)
    
    while True:
        ciudad = input("\n🏙️  Ingrese una ciudad (o 'salir' para terminar): ").strip()
        
        if ciudad.lower() in ["salir", "exit", "quit", ""]:
            print("\n👋 ¡Hasta luego!\n")
            break
        
        pais = input("🌎 Código de país (Enter para CL): ").strip().upper()
        if not pais:
            pais = "CL"
        
        try:
            respuesta = consultar_clima(ciudad, pais)
            mostrar_resultado(respuesta, ciudad)
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
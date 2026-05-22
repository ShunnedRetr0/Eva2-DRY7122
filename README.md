# Evaluación N°2 - DRY7122

**Asignatura:** Desarrollo de Redes Programables  
**Autor:** [Manuel Arrué y Jairo Soto]  
**Fecha:** 21 de Mayo 2026

## Contenido del repositorio

| Carpeta | Descripción |
|---------|-------------|
| `parte2/` | Consumo de API pública (OpenWeatherMap) |
| `parte4/` | Control de credenciales con Flask + SQLite |

## Parte 2: API Pública - OpenWeatherMap

**Nota:** Se utilizó OpenWeatherMap en reemplazo de MapQuest, ya que esta última actualmente requiere ingresar datos de tarjeta de crédito incluso para el plan gratuito.

Script en Python que consume la API pública de OpenWeatherMap para consultar el clima de cualquier ciudad del mundo.

### Ejecución
```bash
cd parte2
pip3 install requests
export OPENWEATHER_API_KEY="tu_api_key"
python3 clima.py
```

## Parte 4: Control de Credenciales

Servicio REST construido con Flask que permite:
- Registrar usuarios con contraseña hasheada (PBKDF2-SHA256)
- Validar credenciales contra base de datos SQLite
- Listar usuarios sin exponer contraseñas

### Ejecución
```bash
cd parte4
pip3 install flask werkzeug
python3 claves.py
```

### Pruebas con curl
```bash
# Registrar usuario
curl -X POST http://localhost:5000/registrar \
  -H "Content-Type: application/json" \
  -d '{"usuario": "pedro", "password": "clave123"}'

# Validar credenciales
curl -X POST http://localhost:5000/validar \
  -H "Content-Type: application/json" \
  -d '{"usuario": "pedro", "password": "clave123"}'
```

## Tecnologías utilizadas

- Python 3
- Flask (microframework web)
- SQLite (base de datos)
- Werkzeug (hashing de contraseñas)
- Requests (cliente HTTP)

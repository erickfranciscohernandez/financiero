# 📚 Diccionario de Problemas - Guía de Uso

Sistema completo para que técnicos de soporte consulten soluciones a problemas comunes de Software, Hardware, Accesos y DLP.

## 📋 Contenido

- **issues_dictionary.json** - Base de datos con todos los problemas
- **issues_dictionary.html** - Interfaz web interactiva
- **issues_api.py** - API REST para acceso programático

---

## 🌐 Interfaz Web (issues_dictionary.html)

### Características

✅ Interfaz moderna y responsive  
✅ Búsqueda de texto completo  
✅ Filtros por categoría, severidad e ID  
✅ Estadísticas en tiempo real  
✅ Diseño atractivo con iconografía clara  

### Cómo Usar

1. **Abrir el archivo**
   ```bash
   # En el navegador
   file:///path/to/issues_dictionary.html
   # O desde localhost si tienes servidor web
   http://localhost:8000/issues_dictionary.html
   ```

2. **Buscar Problema**
   - Ingresa palabra clave: "contraseña", "disco lleno", "API", etc.
   - Sistema busca en: título, descripción, síntomas y soluciones

3. **Filtrar Resultados**
   - **Categoría**: Software, Hardware, Accesos, DLP
   - **Severidad**: Crítica, Alta, Media
   - **ID**: Busca directo por código (SW001, HW002, etc.)

4. **Ver Detalles**
   - Cada problema muestra:
     - ID único
     - Título descriptivo
     - Descripción detallada
     - Síntomas para identificar
     - Soluciones paso a paso
     - Nivel de severidad

### Categorías Disponibles

#### 🔧 **Software** (5 problemas)
- Aplicación no inicia
- API retorna error 500
- Lentitud en reportes
- Integración con API externa
- Conflicto de versiones

#### ⚙️ **Hardware** (5 problemas)
- Disco duro lleno
- Fallo de memoria
- Problemas de conectividad
- CPU al 100%
- Fallo de base de datos

#### 🔐 **Accesos** (5 problemas)
- Problema de autenticación
- Permisos insuficientes
- Token/sesión expirado
- VPN no conecta
- LDAP/Active Directory no sincroniza

#### 🛡️ **DLP** (5 problemas)
- Intento de exfiltración
- Clasificación incorrecta
- Datos borrados sin autorización
- Transferencia a ubicación no autorizada
- Contraseña en logs

---

## 🔌 API REST (issues_api.py)

### Requisitos

```bash
pip install flask flask-cors
```

### Iniciar la API

```bash
python issues_api.py
```

La API estará disponible en: **http://localhost:5000**

### Endpoints

#### 1️⃣ **Obtener Todos los Problemas**

```bash
GET /api/problems
```

**Parámetros (opcionales):**
- `category`: Software, Hardware, Accesos, DLP
- `severity`: critical, high, medium
- `search`: texto a buscar

**Ejemplo:**
```bash
curl "http://localhost:5000/api/problems?category=Software&severity=critical"
```

**Respuesta:**
```json
{
  "count": 2,
  "problems": [
    {
      "id": "SW001",
      "category": "Software",
      "title": "Aplicación no inicia",
      "description": "La aplicación financiera no abre",
      "symptoms": [...],
      "solutions": [...],
      "severity": "critical"
    }
  ]
}
```

#### 2️⃣ **Obtener Problema Específico**

```bash
GET /api/problems/{id}
```

**Ejemplo:**
```bash
curl "http://localhost:5000/api/problems/SW001"
```

**Respuesta:**
```json
{
  "id": "SW001",
  "category": "Software",
  "title": "Aplicación no inicia",
  ...
}
```

#### 3️⃣ **Listar Categorías**

```bash
GET /api/categories
```

**Ejemplo:**
```bash
curl "http://localhost:5000/api/categories"
```

**Respuesta:**
```json
{
  "categories": [
    ["Accesos", 5],
    ["DLP", 5],
    ["Hardware", 5],
    ["Software", 5]
  ]
}
```

#### 4️⃣ **Estadísticas**

```bash
GET /api/statistics
```

**Respuesta:**
```json
{
  "total_problems": 20,
  "by_category": {
    "Software": 5,
    "Hardware": 5,
    "Accesos": 5,
    "DLP": 5
  },
  "by_severity": {
    "critical": 7,
    "high": 10,
    "medium": 3
  },
  "critical_count": 7,
  "high_count": 10,
  "medium_count": 3
}
```

#### 5️⃣ **Búsqueda Avanzada**

```bash
POST /api/search
Content-Type: application/json

{
  "query": "contraseña",
  "category": "Accesos",
  "severity": "high",
  "limit": 10
}
```

**Ejemplo con curl:**
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "disco",
    "category": "Hardware",
    "limit": 5
  }'
```

#### 6️⃣ **Estado de la API**

```bash
GET /api/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "problems_loaded": 20
}
```

#### 7️⃣ **Exportar Todo**

```bash
GET /api/export
```

Descarga todos los problemas en JSON.

---

## 📊 Estructura de Datos (JSON)

```json
{
  "problems": [
    {
      "id": "SW001",
      "category": "Software",
      "title": "Titulo del problema",
      "description": "Descripción detallada",
      "symptoms": [
        "Síntoma 1",
        "Síntoma 2"
      ],
      "solutions": [
        "Solución 1",
        "Solución 2"
      ],
      "severity": "critical|high|medium"
    }
  ]
}
```

**Campos:**
- `id`: Código único (SW001, HW002, ACC003, DLP004, etc.)
- `category`: Categoría del problema
- `title`: Título descriptivo
- `description`: Descripción detallada
- `symptoms`: Lista de síntomas para identificar
- `solutions`: Lista de soluciones paso a paso
- `severity`: critical, high, o medium

---

## 💡 Ejemplos de Uso

### Para Técnicos (Interfaz Web)

1. Usuario reporta: "Mi aplicación no abre"
   - Abrir issues_dictionary.html
   - Buscar: "aplicación no inicia"
   - Ver síntomas y seguir soluciones

2. Usuario reporta: "Mi sesión se cerró de repente"
   - Filtrar por: Categoría = Accesos
   - Buscar: "sesión expirado"
   - Seguir soluciones paso a paso

### Para Desarrolladores (API)

**Python:**
```python
import requests

# Buscar problemas críticos
response = requests.get(
    'http://localhost:5000/api/problems',
    params={'severity': 'critical'}
)
problems = response.json()
print(f"Total críticos: {problems['count']}")

# Obtener problema específico
response = requests.get('http://localhost:5000/api/problems/SW001')
problem = response.json()
print(f"Soluciones para {problem['title']}:")
for sol in problem['solutions']:
    print(f"  - {sol}")
```

**JavaScript:**
```javascript
// Buscar en la aplicación web
fetch('/api/problems?category=Hardware')
  .then(r => r.json())
  .then(data => {
    console.log(`${data.count} problemas de hardware encontrados`);
    data.problems.forEach(p => console.log(p.title));
  });

// Búsqueda avanzada
fetch('/api/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'contraseña',
    severity: 'critical'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 🔄 Integración en Tu Aplicación

### Opción 1: Interfaz Web Integrada

```html
<!-- En tu página de soporte -->
<iframe src="issues_dictionary.html" 
        width="100%" 
        height="800px"
        frameborder="0"></iframe>
```

### Opción 2: API en tu Aplicación

```python
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/support')
def support_page():
    # Obtener problemas de la API
    response = requests.get('http://localhost:5000/api/statistics')
    stats = response.json()
    return render_template('support.html', stats=stats)
```

### Opción 3: Widget en la Aplicación

```javascript
// Cargar diccionario en modal o sidebar
document.getElementById('help-button').addEventListener('click', () => {
  fetch('/api/problems')
    .then(r => r.json())
    .then(data => showHelpModal(data.problems));
});
```

---

## 📝 Agregar Nuevos Problemas

Edita `issues_dictionary.json` y agrega un nuevo objeto al array `problems`:

```json
{
  "id": "SW006",
  "category": "Software",
  "title": "Nueva problema",
  "description": "Descripción",
  "symptoms": [
    "Síntoma 1",
    "Síntoma 2"
  ],
  "solutions": [
    "Solución 1",
    "Solución 2"
  ],
  "severity": "high"
}
```

Recuerda:
- IDs únicos (SW, HW, ACC, DLP seguidos de número)
- Severidad: critical, high, medium
- Mínimo 2 síntomas y 2 soluciones

---

## 🚀 Despliegue en Producción

### Como Servicio Systemd

```bash
# /etc/systemd/system/issues-api.service
[Unit]
Description=Issues Dictionary API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/www/financiero
ExecStart=/usr/bin/python3 /home/www/financiero/issues_api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start issues-api
sudo systemctl enable issues-api
```

### Con Nginx

```nginx
upstream issues_api {
    server localhost:5000;
}

server {
    listen 80;
    server_name support.company.com;

    location /api/ {
        proxy_pass http://issues_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        alias /home/www/financiero/;
    }
}
```

---

## 📊 Monitoreo y Logs

La API genera logs de todas las búsquedas. Para auditoría, puedes:

```python
# Agregar logging a issues_api.py
import logging

logging.basicConfig(
    filename='issues_api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/api/search', methods=['POST'])
def search_problems():
    logging.info(f'Search query: {req_data}')
    # ... rest of code
```

---

## ✅ Checklist de Implementación

- [x] Crear archivo issues_dictionary.json
- [x] Crear interfaz web issues_dictionary.html
- [x] Crear API REST issues_api.py
- [x] Documentar categorías
- [x] Documentar endpoints
- [x] Proporcionar ejemplos de uso
- [ ] Integrar en aplicación principal
- [ ] Entrenar a técnicos
- [ ] Configurar en producción
- [ ] Establecer proceso de actualización

---

## 💬 Soporte

Para preguntas sobre el diccionario:
1. Consulta este README
2. Revisa ejemplos en secciones anteriores
3. Prueba los endpoints en Postman/curl
4. Contesta al equipo de desarrollo

---

## 📄 Licencia

Documento interno - Uso restringido a equipo de soporte técnico.

---

**Última actualización:** Mayo 2026  
**Versión:** 1.0

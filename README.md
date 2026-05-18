# Newsletter Estratégico

Sistema automatizado para generar un newsletter diario basado en la actividad del repositorio de GitHub.

## Características

- 📰 **Generación automática diaria** de newsletter en HTML
- 🔄 **Actualización automática** de commits mediante GitHub API
- 🎨 **Diseño profesional** con tipografía y estilos personalizados
- 🚀 **Ejecución automática** con GitHub Actions

## Estructura del Proyecto

```
.
├── generate_newsletter.py      # Script que genera el newsletter
├── newsletter.html             # Newsletter generado (se actualiza diariamente)
├── .github/
│   └── workflows/
│       └── generate-newsletter.yml  # Workflow de GitHub Actions
└── README.md                   # Este archivo
```

## Cómo Funciona

### Generación Manual

Para generar el newsletter manualmente:

```bash
python generate_newsletter.py
```

El script:
1. Obtiene los commits del último día usando la API de GitHub
2. Formatea la información
3. Genera un archivo `newsletter.html` con el contenido

### Automatización con GitHub Actions

El workflow `generate-newsletter.yml`:

- **Ejecuta diariamente** a las 09:00 UTC
- **Se puede ejecutar manualmente** desde la pestaña Actions
- **Actualiza automáticamente** el archivo `newsletter.html`
- **Hace commit** con los cambios

### Variables de Entorno

El script utiliza:
- `GITHUB_TOKEN`: Token de autenticación (se proporciona automáticamente en GitHub Actions)

## Personalización

### Cambiar la Hora de Ejecución

Edita `.github/workflows/generate-newsletter.yml` y modifica la línea `cron`:

```yaml
- cron: '0 9 * * *'  # Actualmente: 09:00 UTC, todos los días
```

Formatos de cron comunes:
- `'0 9 * * *'` - 09:00 UTC diariamente
- `'0 */6 * * *'` - Cada 6 horas
- `'0 0 * * 1'` - Cada lunes a las 00:00 UTC

### Cambiar Repositorio Monitoreado

Edita `generate_newsletter.py`:

```python
REPO_OWNER = 'usuario'  # Cambiar propietario
REPO_NAME = 'repositorio'  # Cambiar nombre del repositorio
```

## Requisitos

- Python 3.11+
- Librería `requests`: `pip install requests`

## Flujo de Trabajo

1. **GitHub Actions** ejecuta el workflow diariamente
2. El workflow ejecuta `generate_newsletter.py`
3. El script obtiene datos de GitHub API
4. Se genera `newsletter.html`
5. Los cambios se hacen commit automáticamente

## Visualización

### Localmente

Para ver el newsletter generado, abre `newsletter.html` en tu navegador.

### En Línea (Público)

El proyecto incluye una página de inicio (`index.html`) que redirige al newsletter.

**Para publicar en línea con GitHub Pages:**

1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings** → **Pages**
3. En "Source", selecciona:
   - Branch: `main` (o tu rama por defecto)
   - Folder: `/ (root)`
4. Haz clic en **Save**

Tu newsletter estará disponible en:
```
https://<tu-usuario>.github.io/<nombre-repo>/
```

Por ejemplo:
```
https://erickfranciscohernandez.github.io/financiero/
```

## Acceso Público

Una vez habilitadas las Pages:

- **Página de inicio:** https://erickfranciscohernandez.github.io/financiero/
- **Newsletter actual:** https://erickfranciscohernandez.github.io/financiero/newsletter.html
- **Compartir con otros:** Puedes compartir el enlace públicamente

## Notas

- La información se obtiene de los últimos 24 horas
- El script maneja automáticamente errores de conexión
- El token de GitHub se usa para aumentar los límites de rate limiting
- Los cambios se publican automáticamente mediante GitHub Pages
- El newsletter se actualiza diariamente a las 09:00 UTC

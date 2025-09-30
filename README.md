# 🚀 HubSpot Clone Project

## 📋 Descripción

Este proyecto contiene un análisis completo y clonación de la aplicación HubSpot, incluyendo:

- **Aplicación clonada** sin certificados de código
- **Documentación completa** del análisis de la aplicación
- **Scripts de automatización** para modificar y ejecutar la aplicación
- **Análisis de endpoints** y estructura de backend
- **Esquemas de base de datos** y arquitectura

## 🎯 Características

### ✅ **Aplicación Clonada**
- Aplicación HubSpot completamente clonada (138.3 MB)
- Todos los certificados de código eliminados
- Modificaciones aplicadas (nombre, bundle ID, versión)
- 126 frameworks y 4 plugins sin firmas

### 📚 **Documentación Completa**
- Análisis de endpoints y APIs
- Estructura de base de datos
- Arquitectura de backend
- Componentes de UI y frontend
- Integraciones y servicios externos

### 🔧 **Scripts de Automatización**
- `launch_hubspot_unsigned.py` - Crear versión sin certificados
- `run_clone_app.py` - Ejecutar aplicación clonada
- `remove_certificates.sh` - Eliminar certificados manualmente

## 🚀 Uso Rápido

### Ejecutar HubSpot Original
```bash
open /Applications/HubSpot.app
```

### Crear Versión Sin Certificados
```bash
cd hubspot-clone
python3 launch_hubspot_unsigned.py
```

### Ejecutar Aplicación Clonada
```bash
cd hubspot-clone
python3 run_clone_app.py
```

## 📁 Estructura del Proyecto

```
hs/
├── hubspot-clone/           # Aplicación clonada
│   ├── HubSpot.app/         # Aplicación sin certificados
│   ├── documentation/       # Documentación completa
│   ├── *.py                # Scripts de automatización
│   └── .gitignore          # Archivos ignorados
├── README.md               # Este archivo
└── .gitignore             # Configuración de Git
```

## 📖 Documentación

La documentación completa está disponible en la carpeta `documentation/`:

- **API Analysis** - Análisis de endpoints y APIs
- **Backend Structure** - Arquitectura y patrones de backend
- **Database Schema** - Esquemas y estructuras de datos
- **Frontend Components** - Componentes de UI y UX
- **Integrations** - Servicios externos y APIs

## ⚠️ Consideraciones Legales

Este proyecto es únicamente para fines educativos y de investigación. La aplicación clonada no debe ser utilizada para propósitos comerciales sin la autorización correspondiente de HubSpot.

## 🔧 Requisitos

- macOS (para ejecutar la aplicación original)
- Python 3.x (para los scripts)
- Xcode (opcional, para simulador iOS)

## 📝 Licencia

Este proyecto es para fines educativos únicamente.

## 🤝 Contribuciones

Este es un proyecto de análisis y clonación educativa. Las contribuciones deben seguir las mejores prácticas de desarrollo y respetar los términos de uso de las aplicaciones originales.

---

**Nota**: Este proyecto contiene una aplicación clonada de HubSpot con todos los certificados de código eliminados para fines de análisis y aprendizaje.

#!/bin/bash

# Script para ejecutar HubSpot con modificaciones
echo "🚀 Iniciando HubSpot modificado..."

# Verificar si la app original está instalada
if [ ! -d "/Applications/HubSpot.app" ]; then
    echo "❌ HubSpot no está instalado en /Applications/"
    exit 1
fi

# Crear un directorio temporal para modificaciones
TEMP_DIR="/tmp/hubspot-modified-$$"
mkdir -p "$TEMP_DIR"

echo "📁 Creando copia temporal en: $TEMP_DIR"

# Copiar la aplicación original
cp -r "/Applications/HubSpot.app" "$TEMP_DIR/"

# Aplicar modificaciones
echo "🔧 Aplicando modificaciones..."

# Cambiar el nombre de la aplicación
plutil -replace CFBundleDisplayName -string "HubSpot Modificado" "$TEMP_DIR/HubSpot.app/Wrapper/HubSpot.app/Info.plist"

# Agregar un mensaje personalizado
echo "✅ Modificaciones aplicadas:"
echo "   - Nombre cambiado a: HubSpot Modificado"
echo "   - Ubicación temporal: $TEMP_DIR"

# Ejecutar la aplicación modificada
echo "🎯 Ejecutando HubSpot modificado..."
open "$TEMP_DIR/HubSpot.app"

echo "✨ ¡HubSpot modificado iniciado!"
echo "💡 La aplicación se ejecutará con las modificaciones aplicadas"

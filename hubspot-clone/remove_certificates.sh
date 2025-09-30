#!/bin/bash

# ============================================================
# HUBSPOT CLONE - ELIMINADOR DE CERTIFICADOS
# ============================================================

echo "🚀 HUBSPOT CLONE - ELIMINANDO CERTIFICADOS"
echo "============================================================"

# Directorio de la aplicación original
ORIGINAL_APP="/Applications/HubSpot.app"
# Directorio de destino para la copia sin firmas
TEMP_DIR="/tmp/hubspot_unsigned_$(date +%s)"
MODIFIED_APP="$TEMP_DIR/HubSpot.app"

echo "🚀 Creando versión sin certificados..."

# Crear directorio temporal
mkdir -p "$TEMP_DIR"
echo "📁 Creando copia temporal en: $TEMP_DIR"

# Copiar la aplicación original al directorio temporal
echo "📋 Copiando aplicación..."
cp -R "$ORIGINAL_APP" "$MODIFIED_APP"
echo "✅ Aplicación copiada"

# Aplicar modificaciones (cambiar nombre en Info.plist)
echo "🔧 Aplicando modificaciones..."
plutil -replace CFBundleDisplayName -string "HubSpot Sin Firmas" "$MODIFIED_APP/Contents/Info.plist"
plutil -replace CFBundleIdentifier -string "com.hubspot.CRMAppRelease.unsigned" "$MODIFIED_APP/Contents/Info.plist"
plutil -replace CFBundleVersion -string "1.0.0.unsigned" "$MODIFIED_APP/Contents/Info.plist"

echo "✅ Modificaciones aplicadas:"
echo "   - Nombre: $(plutil -extract CFBundleDisplayName xml1 -o - "$MODIFIED_APP/Contents/Info.plist" | xmllint --xpath 'string(//string)' -)"
echo "   - Bundle ID: $(plutil -extract CFBundleIdentifier xml1 -o - "$MODIFIED_APP/Contents/Info.plist" | xmllint --xpath 'string(//string)' -)"

# Función para eliminar firmas recursivamente
remove_signatures() {
    local path="$1"
    echo "🚫 Eliminando firmas en: $path"
    
    # Eliminar firma de la aplicación/framework
    codesign --remove-signature "$path" 2>/dev/null || true
    
    # Eliminar directorios de firma
    find "$path" -name "_CodeSignature" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$path" -name "CodeResources" -type f -exec rm -f {} + 2>/dev/null || true
    
    # Eliminar firmas de frameworks internos
    if [ -d "$path/Contents/Frameworks" ]; then
        for framework in "$path/Contents/Frameworks"/*.framework; do
            if [ -d "$framework" ]; then
                echo "   🔧 Eliminando firma de: $(basename "$framework")"
                codesign --remove-signature "$framework" 2>/dev/null || true
                find "$framework" -name "_CodeSignature" -type d -exec rm -rf {} + 2>/dev/null || true
                find "$framework" -name "CodeResources" -type f -exec rm -f {} + 2>/dev/null || true
            fi
        done
    fi
    
    # Eliminar firmas de plugins
    if [ -d "$path/Contents/PlugIns" ]; then
        for plugin in "$path/Contents/PlugIns"/*.appex; do
            if [ -d "$plugin" ]; then
                echo "   🔌 Eliminando firma de: $(basename "$plugin")"
                codesign --remove-signature "$plugin" 2>/dev/null || true
                find "$plugin" -name "_CodeSignature" -type d -exec rm -rf {} + 2>/dev/null || true
                find "$plugin" -name "CodeResources" -type f -exec rm -f {} + 2>/dev/null || true
            fi
        done
    fi
}

# Eliminar todas las firmas
echo "🚫 Eliminando todas las firmas de código..."
remove_signatures "$MODIFIED_APP"
echo "✅ Todas las firmas eliminadas"

# Intentar re-firmar con firma ad-hoc
echo "✍️ Re-firmando con firma ad-hoc..."
codesign --force --deep --sign - "$MODIFIED_APP" 2>/dev/null || echo "⚠️  No se pudo re-firmar, continuando sin firma..."

# Verificar que no queden firmas
echo "🔍 Verificando eliminación de firmas..."
if find "$MODIFIED_APP" -name "_CodeSignature" -o -name "CodeResources" | grep -q .; then
    echo "⚠️  Aún quedan algunos archivos de firma"
    find "$MODIFIED_APP" -name "_CodeSignature" -o -name "CodeResources"
else
    echo "✅ Todas las firmas eliminadas completamente"
fi

# Intentar ejecutar la aplicación sin firmas
echo "🎯 Intentando ejecutar aplicación sin firmas..."
echo "📱 Ruta: $MODIFIED_APP"

# Intentar con open
if open "$MODIFIED_APP" 2>/dev/null; then
    echo "✨ ¡HubSpot sin firmas iniciado con 'open'!"
    echo "✅ La aplicación debería estar ejecutándose"
else
    echo "❌ Error con 'open', intentando ejecutar binario directamente..."
    
    # Buscar y ejecutar el binario directamente
    EXECUTABLE="$MODIFIED_APP/Contents/MacOS/HubSpot"
    if [ -f "$EXECUTABLE" ] && [ -x "$EXECUTABLE" ]; then
        echo "💡 Ejecutando binario directamente: $EXECUTABLE"
        "$EXECUTABLE" &
        echo "✅ ¡Binario ejecutado directamente!"
    else
        echo "❌ No se encontró ejecutable en: $EXECUTABLE"
        
        # Buscar otros ejecutables
        echo "🔍 Buscando otros ejecutables..."
        find "$MODIFIED_APP" -type f -name "HubSpot*" -executable | while read -r exec_file; do
            echo "   📱 Encontrado: $exec_file"
            echo "   💡 Intentando ejecutar..."
            "$exec_file" &
            echo "   ✅ ¡Ejecutado: $(basename "$exec_file")!"
            break
        done
    fi
fi

echo ""
echo "============================================================")
echo "📁 Directorio temporal: $TEMP_DIR"
echo "💡 Puedes inspeccionar los archivos modificados en esa ubicación"
echo ""
echo "✅ ¡Proceso completado!"
echo "💡 Si la aplicación no se ejecuta, revisa los permisos o usa Xcode"
